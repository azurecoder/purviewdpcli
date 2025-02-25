# Summary 

This small comand line utility is built to manipulate Data Products in Purview. It's not really evident what the SDK's are so a lot of this has been reverse-engineered from the new Purview Portal. Data Products are a new concept in the new portal and so the types are not covered in the published Atlas API in the Microsoft Learn Docs.

In order to build a data product you first need a governance domain. Create this in Purview. Once this is done you can add a Data Product to a domain. This is a collection of related assets. This utility will help you create one in Purview.

# Usage 

To list all **Published** Data Products and governance domains simply run the command.

```python
python main.py --dp
```

This should yield an output like this, the governance domain followed by all of the data products within that domain.

```
=== Data Products in Purview for (Tutorial) Personal Health ===
• Covid-19 Vaccination and Case Trending by Age

=== Data Products in Corporate ===
No data products found or an error occurred.
```

I'll have more switches soon as I build in support for CDEs, OKRs, terms and data policies.

The next thing coming is the question bank.