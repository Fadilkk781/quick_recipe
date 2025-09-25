import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Food Recipe Finder",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recipe-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #FF6B6B;
    }
    .ingredient-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .instruction-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .stats-box {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(file_path):
    """Load the recipe dataset from a CSV file."""
    try:
        df = pd.read_csv(r"C:\Users\FADIL\OneDrive\Desktop\food recipe\data\Cleaned_Food_Dataset 1.csv", on_bad_lines='skip')
        return df
    except FileNotFoundError:
        st.error(f"Data file not found. Please ensure 'Cleaned_Food_Dataset 1.csv' is located at: {file_path}")
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def find_recipes(df, food_name, search_type="contains"):
    """
    Find recipes based on search criteria
    """
    if search_type == "contains":
        recipes = df[df['TranslatedRecipeName'].str.contains(food_name, case=False, na=False)]
    else:  # exact match
        recipes = df[df['TranslatedRecipeName'].str.lower() == food_name.lower()]
    
    return recipes

def display_recipe(recipe_row):
    """Display a single recipe in a formatted way"""
    with st.container():
        st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
        
        # Recipe Header
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.subheader(f"{recipe_row['TranslatedRecipeName']}")
        
        with col2:
            st.markdown(f"**Time:** {recipe_row['TotalTimeInMins']} mins")
        
        with col3:
            st.markdown(f"**Cuisine:** {recipe_row['Cuisine']}")
        
        # Recipe Details
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="ingredient-box">', unsafe_allow_html=True)
            st.markdown("### Ingredients")
            ingredients = recipe_row['TranslatedIngredients'].split(',')
            for i, ingredient in enumerate(ingredients, 1):
                st.markdown(f"{i}. {ingredient.strip()}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Additional info
            st.markdown('<div class="stats-box">', unsafe_allow_html=True)
            st.markdown("### Recipe Stats")
            st.markdown(f"**Ingredient Count:** {recipe_row['Ingredient-count']}")
            if 'Cleaned-Ingredients' in recipe_row:
                cleaned_ingredients = recipe_row['Cleaned-Ingredients'].split(',')
                st.markdown(f"**Main Ingredients:** {', '.join(cleaned_ingredients[:5])}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="instruction-box">', unsafe_allow_html=True)
            st.markdown("### Instructions")
            instructions = recipe_row['TranslatedInstructions']
            # Split instructions into steps for better readability
            steps = instructions.split('.')
            for i, step in enumerate(steps, 1):
                if step.strip():
                    st.markdown(f"**Step {i}:** {step.strip()}.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")

def main():
    # Header
    st.markdown('<h1 class="main-header">Food Recipe Finder</h1>', unsafe_allow_html=True)
    st.markdown("### Discover delicious recipes from around the world!")
    
    # Define the path to the data file
    # Note: Using a relative path like './data/Cleaned_Food_Dataset 1.csv' is often more portable.
    file_path = r'C:\Users\FADIL\OneDrive\Desktop\food recipe\data\Cleaned_Food_Dataset 1.csv'
    
    # Load data
    df = load_data(r"C:\Users\FADIL\OneDrive\Desktop\food recipe\models\food_recipe.pkl")
    
    if df is None:
        st.stop()
    
    # Sidebar for filters and stats
    with st.sidebar:
        st.header("Search & Filters")
        
        # Search options
        search_type = st.selectbox(
            "Search Type",
            ["contains", "exact"],
            help="Choose how to search for recipes"
        )
        
        # Cuisine filter
        cuisines = ['All'] + sorted(df['Cuisine'].unique().tolist())
        selected_cuisine = st.selectbox("Filter by Cuisine", cuisines)
        
        # Time filter
        st.subheader("Cooking Time")
        time_range = st.slider(
            "Maximum cooking time (minutes)",
            min_value=int(df['TotalTimeInMins'].min()),
            max_value=int(df['TotalTimeInMins'].max()),
            value=int(df['TotalTimeInMins'].max()),
            step=5
        )
        
        # Ingredient count filter
        st.subheader("Ingredient Count")
        ingredient_range = st.slider(
            "Maximum number of ingredients",
            min_value=int(df['Ingredient-count'].min()),
            max_value=int(df['Ingredient-count'].max()),
            value=int(df['Ingredient-count'].max()),
            step=1
        )
        
        # Dataset statistics
        st.markdown("---")
        st.subheader("Dataset Statistics")
        st.metric("Total Recipes", len(df))
        st.metric("Total Cuisines", df['Cuisine'].nunique())
        st.metric("Avg Cooking Time", f"{df['TotalTimeInMins'].mean():.0f} mins")
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Search input
        food_name = st.text_input(
            "Enter the recipe name you're looking for:",
            placeholder="e.g., Masala Karela, Biryani, Pasta..."
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
        search_button = st.button("Search Recipes", type="primary")
    
    # Random recipe suggestion
    if st.button("Surprise Me! (Random Recipe)"):
        random_recipe = df.sample(1).iloc[0]
        st.markdown("### Here's a random recipe for you:")
        display_recipe(random_recipe)
    
    # Search and display results
    if food_name or search_button:
        if food_name:
            # Apply filters
            filtered_df = df.copy()
            
            if selected_cuisine != 'All':
                filtered_df = filtered_df[filtered_df['Cuisine'] == selected_cuisine]
            
            filtered_df = filtered_df[filtered_df['TotalTimeInMins'] <= time_range]
            filtered_df = filtered_df[filtered_df['Ingredient-count'] <= ingredient_range]
            
            # Search for recipes
            recipes = find_recipes(filtered_df, food_name, search_type)
            
            if not recipes.empty:
                st.success(f"Found {len(recipes)} recipe(s) matching your search!")
                
                # Sort recipes by relevance (by cooking time)
                recipes = recipes.sort_values(['TotalTimeInMins'])
                
                # Display recipes
                for idx, (_, recipe) in enumerate(recipes.iterrows()):
                    display_recipe(recipe)
                    
                    # Limit display to first 5 recipes if too many results
                    if idx >= 4 and len(recipes) > 5:
                        remaining = len(recipes) - 5
                        st.info(f"... and {remaining} more recipes. Try refining your search for fewer results.")
                        break
            else:
                st.warning(f"No recipes found for '{food_name}' with the current filters. Try:")
                st.markdown("""
                - Checking the spelling
                - Using different search terms
                - Adjusting the filters in the sidebar
                - Using 'contains' search instead of 'exact'
                """)
                
                # Suggest similar recipes
                st.markdown("### You might also like these recipes:")
                similar_recipes = df.sample(3)
                for _, recipe in similar_recipes.iterrows():
                    st.markdown(f"- **{recipe['TranslatedRecipeName']}** ({recipe['Cuisine']} cuisine)")
        else:
            st.info("Please enter a recipe name to search.")
    
    # Popular cuisines section
    st.markdown("---")
    st.markdown("### Explore Popular Cuisines")
    
    cuisine_counts = df['Cuisine'].value_counts().head(8)
    cols = st.columns(4)
    
    for idx, (cuisine, count) in enumerate(cuisine_counts.items()):
        with cols[idx % 4]:
            if st.button(f"{cuisine}\n({count} recipes)", key=f"cuisine_{idx}"):
                cuisine_recipes = df[df['Cuisine'] == cuisine].head(3)
                st.markdown(f"### Top {cuisine} Recipes:")
                for _, recipe in cuisine_recipes.iterrows():
                    st.markdown(f"**{recipe['TranslatedRecipeName']}** - {recipe['TotalTimeInMins']} mins")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>Food Recipe Finder | Built with Streamlit</p>
        <p>Discover, Cook, and Enjoy!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()