import xml.etree.ElementTree as et

tree = et.parse("../ground_truth/ref_anni005.xml")
root = tree.getroot()
for child in root:
    if child.get("type") == "CUT":
        print(child.get("preFNum"))
