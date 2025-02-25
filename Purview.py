import os
import msal
import requests
import yaml

class PurviewDataProducts:

    def __init__(self):  
        yaml = self.load_config_from_yaml("config.yaml")  
        self.TENANT_ID = yaml["TENANT_ID"]
        self.CLIENT_ID = yaml["CLIENT_ID"]
        self.CLIENT_SECRET = yaml["CLIENT_SECRET"]
        self.PURVIEW_ACCOUNT_NAME = yaml["PURVIEW_ACCOUNT_NAME"]
        self.AUTHORITY_URL = f"https://login.microsoftonline.com/{self.TENANT_ID}"
        self.PURVIEW_ENDPOINT = f"https://{self.PURVIEW_ACCOUNT_NAME}.purview.azure.com"
        self.PURVIEW_SCOPE = ["https://purview.azure.net/.default"]

    def load_config_from_yaml(self, yaml_file):
        """
        Reads configuration from a YAML file and returns a dictionary
        of the same structure that you'd otherwise get from environment variables.
        """
        with open(yaml_file, "r") as f:
            config = yaml.safe_load(f) or {}
        
        return {
            "TENANT_ID": config.get("TENANT_ID", ""),
            "CLIENT_ID": config.get("CLIENT_ID", ""),
            "CLIENT_SECRET": config.get("CLIENT_SECRET", ""),
            "PURVIEW_ACCOUNT_NAME": config.get("PURVIEW_ACCOUNT_NAME", "")
        }

    def get_purview_token(self):
        """
        Uses MSAL to authenticate and retrieve an access token for Azure Purview.
        Returns the access token string.
        """
        app = msal.ConfidentialClientApplication(
            self.CLIENT_ID,
            authority = self.AUTHORITY_URL,
            client_credential = self.CLIENT_SECRET
        )

        result = app.acquire_token_for_client(scopes = self.PURVIEW_SCOPE)
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception(f"Could not acquire token. Error: {result.get('error_description')}")


    def list_data_products_in_purview(self, asset_guid, limit=50):
        """
        Lists assets in Purview of the given asset_type using the new Data Map search API.
        By default, looks for a custom type named 'DataProduct'.
        If your data products are registered as 'azure_blob' or some other type, pass that in.
        """
        
        token = self.get_purview_token()

        url = f"{self.PURVIEW_ENDPOINT}/datagovernance/catalog/dataproducts/query"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
           "domainIds":[asset_guid],"skip":0,"top":25,"status":"Published"
        }

        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code != 200:
            print(f"Failed to list data products. Status Code: {resp.status_code}")
            print("Response:", resp.text)
            return []

        data = resp.json()
        items = data.get("value", [])
        if not items:
            print(f"No assets found for asset type '{asset_guid}'.")
            return []

        product_names = []
        for item in items:
            product_names.append(item.get("name"))

        return product_names

    def list_governance_domains(self):
        """
        Fetches a list of published governance domains from the Purview Data Governance API.
        Returns a dictionary in the form { domain_name: domain_guid } 
        where only domains with status == 'Published' are included.
        """
        token = self.get_purview_token()

        url = f"{self.PURVIEW_ENDPOINT}/datagovernance/catalog/businessdomains"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed to retrieve governance domains.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)
            return {}

        data = response.json()
        values = data.get("value", [])

        domains_dict = {}
        for domain in values:
            if domain.get("status") == "Published":
                name = domain.get("name")
                guid = domain.get("id")
                if name and guid:
                    domains_dict[name] = guid

        return domains_dict

