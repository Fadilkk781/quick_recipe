import streamlit as st
import pandas as pd
import base64
import pickle

# Set page configuration
st.set_page_config(
    page_title="Food Recipe Finder",
    # Note: Using a relative path for the icon.
    # Make sure 'log.png' is in the same directory as your script.
    page_icon="log.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

def add_bg_from_local(image_path):
    """Add background image from local file"""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        # If image not found, use a fallback gradient background
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                background-attachment: fixed;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

# Add background image - Using a relative path.
# Make sure 'hi.png' is in the same directory as your script.
add_bg_from_local('hi.png')

# Enhanced CSS with animations and new styles for expanders
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
            
    .food-card {
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.12) 0%,
        rgba(255, 255, 255, 0.06) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 0; /* Changed from 0.5rem to 0 to fit inside expander */
    transition: all 0.4s ease;
    animation: slideIn 0.6s ease-out;
    position: relative;
    overflow: hidden;
    z-index: 1;
}

.food-card:hover {
    transform: translateY(-8px) scale(1.02);
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.18) 0%,
        rgba(255, 255, 255, 0.12) 100%);
    box-shadow: 0 15px 40px rgba(255, 255, 255, 0.15);
}

.food-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, 
        transparent, 
        rgba(255, 255, 255, 0.15), 
        transparent);
    transition: left 0.6s;
}

.main-header {
    font-size: 4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 2rem;
    animation: fadeInDown 1s ease-out;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.2);

    /* --- Added Code --- */
    background-color: #f0f4f0; /* A light green-tinted background */
    padding: 2rem;            /* Adds space around the text */
    border-radius: 10px;      /* Rounds the corners of the background */
}
    
    .subheader {
        text-align: center;
        color: #555;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        animation: fadeIn 1.2s ease-out;
    }
    
    .recipe-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        animation: slideUp 0.5s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .recipe-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8787 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
    
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.9);
        border: 2px solid #FF6B6B;
        border-radius: 30px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF8787;
        box-shadow: 0 0 0 2px rgba(255, 107, 107, 0.2);
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    
    .recipe-title {
        color: #FF6B6B;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s ease-out;
    }
    
    .recipe-meta {
        background: rgba(255, 107, 107, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.25rem;
        animation: fadeIn 0.7s ease-out;
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #FF6B6B, transparent);
        margin: 2rem 0;
    }

    /* --- NEW CSS for Liquid Design Expander --- */
   div[data-testid="stExpander"] {
        border-radius: 15px !important;
        border: 1px solid #FFD8D8 !important;
        overflow: hidden;
        margin-top: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: box-shadow 0.3s ease-in-out;
   }

   div[data-testid="stExpander"]:hover {
       box-shadow: 0 8px 25px rgba(0,0,0,0.1);
   }

   div[data-testid="stExpander"] summary {
       padding: 0.75rem 1rem;
       background-color: #FFF5F5;
       color: #FF6B6B;
       font-weight: 600;
       font-size: 1.1rem;
       transition: background-color 0.3s ease;
   }

   div[data-testid="stExpander"] summary:hover {
        background-color: #FFECEC;
   }
    
    /* Remove default padding from expander content area */
   div[data-testid="stExpanderDetails"] {
       padding: 0 !important;
   }

</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(file_path=None, pickle_path=None):
    """Load the recipe dataset from CSV or pickle file."""
    try:
        if pickle_path:
            with open(pickle_path, 'rb') as f:
                df = pickle.load(f)
                return df
        elif file_path:
            df = pd.read_csv(file_path, on_bad_lines='skip')
            return df
    except FileNotFoundError:
        st.error(f"Data file not found. Please check the file path and ensure the data files are in the correct directory.")
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def find_recipes(df, food_name, search_type="contains"):
    """Find recipes based on search criteria"""
    if not food_name:
        return pd.DataFrame()
    
    food_name = food_name.strip()
    
    if search_type == "contains":
        mask = df['TranslatedRecipeName'].astype(str).str.contains(food_name, case=False, na=False, regex=False)
        recipes = df[mask]
    else:  # exact match
        mask = df['TranslatedRecipeName'].astype(str).str.lower() == food_name.lower()
        recipes = df[mask]
    
    return recipes

def display_recipe(recipe_row):
    """Display a single recipe with an enhanced, liquid design using expanders"""
    with st.container():
        st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
        
        # Recipe Header
        st.markdown(f'<h2 class="recipe-title">{recipe_row["TranslatedRecipeName"]}</h2>', unsafe_allow_html=True)
        
        # Recipe metadata badges
        meta_cols = st.columns(3)
        with meta_cols[0]:
            st.markdown(f'<span class="recipe-meta">Time: {recipe_row["TotalTimeInMins"]} mins</span>', unsafe_allow_html=True)
        with meta_cols[1]:
            st.markdown(f'<span class="recipe-meta">{recipe_row["Cuisine"]} Cuisine</span>', unsafe_allow_html=True)
        with meta_cols[2]:
            st.markdown(f'<span class="recipe-meta">{recipe_row["Ingredient-count"]} Ingredients</span>', unsafe_allow_html=True)

        # --- MODIFIED SECTION FOR INGREDIENTS ---
        with st.expander("View Ingredients"):
            ingredients = [ing.strip() for ing in str(recipe_row['TranslatedIngredients']).split(',')]
            
            # Split the list into two for the columns
            mid_point = (len(ingredients) + 1) // 2
            col1_ingredients = ingredients[:mid_point]
            col2_ingredients = ingredients[mid_point:]
            
            # Build the HTML for each column's list items
            col1_html = "".join([f"<li>{ing}</li>" for ing in col1_ingredients])
            col2_html = "".join([f"<li>{ing}</li>" for ing in col2_ingredients])

            # Combine everything into a single HTML block to apply the .food-card style correctly
            full_html = f"""
            <div class="food-card">
                <div style="display: flex; flex-direction: row; gap: 2rem;">
                    <ul style="flex: 1; padding-left: 20px; margin: 0;">{col1_html}</ul>
                    <ul style="flex: 1; padding-left: 20px; margin: 0;">{col2_html}</ul>
                </div>
            </div>
            """
            st.markdown(full_html, unsafe_allow_html=True)

        # --- MODIFIED SECTION FOR INSTRUCTIONS ---
        with st.expander("View Instructions"):
            instructions = str(recipe_row['TranslatedInstructions'])
            steps = [s.strip() for s in instructions.split('.') if s.strip()]

            if not steps:
                # Fallback for instructions without periods
                instructions_html = f'<div class="food-card"><p>{instructions}</p></div>'
            else:
                # Build an ordered list for the steps
                steps_html = "".join([f"<li>{step}.</li>" for step in steps])
                instructions_html = f'<div class="food-card"><ol style="padding-left: 20px; margin: 0;">{steps_html}</ol></div>'

            st.markdown(instructions_html, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)


def main():
    st.markdown('<h1 class="main-header">Explorer Your Taste</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Discover Amazing Recipes From Around The World</p>', unsafe_allow_html=True)
    
    # Using relative paths for data files.
    # Create a 'data' folder for the CSV and a 'models' folder for the pickle file.
    csv_path = 'data/Cleaned_Food_Dataset 1.csv'
    pickle_path = 'models/food_recipe.pkl'
    
    # Try loading from pickle first, then CSV
    df = load_data(pickle_path=pickle_path)
    if df is None:
        df = load_data(file_path=csv_path)
    
    if df is None:
        st.stop()
    
    with st.sidebar:
        st.markdown("## Search & Filters")
        st.markdown("---")
        
        search_type = st.selectbox(
            "Search Type",
            ["contains", "exact"],
            help="'Contains' finds recipes with the keyword anywhere in the name. 'Exact' matches the name precisely."
        )
        
        cuisines = ['All'] + sorted(df['Cuisine'].dropna().unique().tolist())
        selected_cuisine = st.selectbox("Filter by Cuisine", cuisines)
        
        st.markdown("### Cooking Time")
        time_range = st.slider(
            "Maximum time (minutes)",
            min_value=0, # Start from 0 for clarity
            max_value=int(df['TotalTimeInMins'].max()),
            value=120,
            step=5
        )
        
        st.markdown("### Ingredient Count")
        ingredient_range = st.slider(
            "Maximum ingredients",
            min_value=0, # Start from 0
            max_value=int(df['Ingredient-count'].max()),
            value=20,
            step=1
        )
        
        st.markdown("---")
        st.markdown("### Dataset Statistics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Recipes", f"{len(df):,}")
            st.metric("Avg Time", f"{df['TotalTimeInMins'].mean():.0f} min")
        with col2:
            st.metric("Cuisines", df['Cuisine'].nunique())
            st.metric("Avg Ingredients", f"{df['Ingredient-count'].mean():.0f}")
    
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        food_name = st.text_input(
            "Search for your favorite recipe:",
            placeholder="Try: Masala, Biryani, Pasta, Curry, Salad...",
            key="search_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("Search", type="primary", key="search_btn")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Surprise Me with a Random Recipe!", key="random_btn", use_container_width=True):
            random_recipe = df.sample(1).iloc[0]
            st.session_state.random_recipe = random_recipe
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if 'random_recipe' in st.session_state:
        st.markdown("### Your Random Recipe Selection:")
        display_recipe(st.session_state.random_recipe)
        del st.session_state.random_recipe # Clear after displaying
    
    if search_button and food_name:
        filtered_df = df.copy()
        
        if selected_cuisine != 'All':
            filtered_df = filtered_df[filtered_df['Cuisine'] == selected_cuisine]
        
        filtered_df = filtered_df[filtered_df['TotalTimeInMins'] <= time_range]
        filtered_df = filtered_df[filtered_df['Ingredient-count'] <= ingredient_range]
        
        recipes = find_recipes(filtered_df, food_name, search_type)
        
        if not recipes.empty:
            st.success(f"Found {len(recipes)} recipe(s) matching your criteria for '{food_name}'")
            
            recipes = recipes.sort_values('TotalTimeInMins')
            
            for idx, (_, recipe) in enumerate(recipes.head(5).iterrows()):
                display_recipe(recipe)
                
            if len(recipes) > 5:
                st.info(f"Showing top 5 results out of {len(recipes)}. Refine your search for more specific results.")
        else:
            st.warning(f"No recipes found for '{food_name}' with the selected filters.")
            st.markdown("""
            **Suggestions:**
            - Try different keywords or check your spelling.
            - Broaden your filters (e.g., increase cooking time).
            - Use the 'contains' search type for more flexible matching.
            """)

if __name__ == "__main__":
    main()
