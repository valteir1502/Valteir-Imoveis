import xml.etree.ElementTree as ET

tree = ET.parse("imoveis.xml")
root = tree.getroot()

for prop in root.findall(".//Listing"):
    title = prop.findtext("Title", "")
    desc = prop.findtext("Description", "")
    price = prop.findtext(".//ListPrice", "")
    neighborhood = prop.findtext(".//Neighborhood", "")
    
    combined = f"{title} {desc} {price} {neighborhood}"
    if "buona vita" in combined.lower():
        print(f"Listing ID: {prop.findtext('ListingID')}")
        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Neighborhood: {neighborhood}")
        print(f"Desc snippet: {desc[:200]}")
        print("-" * 50)
