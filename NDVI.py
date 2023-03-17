import streamlit as st
import ee

# Initialize Earth Engine
ee.Initialize()

# Define the NDVI calculation function
def calculate_ndvi(start_year, end_year):
    # Load the Landsat 8 surface reflectance collection
    collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    
    # Filter the collection by date and location
    filtered = collection.filterDate(f'{start_year}-01-01', f'{end_year}-12-31') \
                        .filterBounds(ee.Geometry.Point(-95.86, 39.06))
    
    # Calculate NDVI for each image in the collection
    def add_ndvi(image):
        ndvi = image.normalizedDifference(['B5', 'B4'])
        return image.addBands(ndvi.rename('NDVI'))
    
    ndvi_collection = filtered.map(add_ndvi)
    
    # Return the NDVI image collection
    return ndvi_collection

# Define the Streamlit app
def app():
    st.title('Normalized Difference Vegetation Index (NDVI) for 2000 to 2023')
    
    # Sidebar inputs
    start_year = st.sidebar.slider('Start year', 2000, 2022, 2000)
    end_year = st.sidebar.slider('End year', 2001, 2023, 2023)
    
    # Calculate NDVI for the selected years
    ndvi_collection = calculate_ndvi(start_year, end_year)
    
    # Show NDVI map
    st.subheader('NDVI Map')
    ndvi_image = ndvi_collection.mean().select('NDVI')
    st.map(ndvi_image, zoom=8)
    
    # Show NDVI chart
    st.subheader('NDVI Chart')
    ndvi_chart = st.line_chart(ndvi_collection.reduceRegion(ee.Reducer.mean(), geometry=ee.Geometry.Point(-95.86, 39.06), scale=30).get('NDVI').getInfo())
    
# Run the app
if __name__ == '__main__':
    app()
