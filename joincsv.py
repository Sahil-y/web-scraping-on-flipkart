import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lists to store the extracted data
Product_name = []
Prices = []
Description = []
Reviews = []

# Loop through pages 2 to 11
for i in range(2, 12):
    url = f"https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3D10000&p%5B%5D=facets.price_range.to%3DMax&page="+str(i)
    r = requests.get(url)
    print(f"Request to {url}: Status code {r.status_code}")
    soup = BeautifulSoup(r.text, "lxml")
    box = soup.find("div", class_="DOjaWF gdgoEp")
    
    if box:
        names = box.find_all("div", class_="KzDlHZ")
        prices = box.find_all("div", class_="Nx9bqj _4b5DiR")
        desc = box.find_all("ul", class_="G4BRas")
        reviews = box.find_all("div", class_="XQDdHH")
        
        print(f"Page {i} - Found {len(names)} names, {len(prices)} prices, {len(desc)} descriptions, {len(reviews)} reviews")
        
        # Ensure all found elements lists have the same length
        min_length = min(len(names), len(prices), len(desc), len(reviews))
        
        for j in range(min_length):
            Product_name.append(names[j].text)
            Prices.append(prices[j].text)
            Description.append(desc[j].text)
            Reviews.append(reviews[j].text)
    else:
        print(f"Box not found on page {i}")

# Check lengths of lists
print(f"Final counts - Product Names: {len(Product_name)}, Prices: {len(Prices)}, Descriptions: {len(Description)}, Reviews: {len(Reviews)}")

# Ensure all lists are of the same length before creating DataFrame
min_length = min(len(Product_name), len(Prices), len(Description), len(Reviews))

df = pd.DataFrame({
    "Product Name": Product_name[:min_length],
    "Prices": Prices[:min_length],
    "Description": Description[:min_length],
    "Reviews": Reviews[:min_length]
})

# Save the DataFrame to a CSV file
df.to_csv('flipkart_products.csv', index=False)
print("Data saved to flipkart_products.csv")

print(df)
