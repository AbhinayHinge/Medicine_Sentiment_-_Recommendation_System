import pickle
import pandas as pd
import altair as alt
import streamlit as st
from textblob import TextBlob

medicine_dict = pickle.load(open('Medicine_dict.pkl','rb'))
medicine=pd.DataFrame(medicine_dict)

# Load and display animated image
with open("animation.html", "r") as f:
    html = f.read()
st.components.v1.html(html, height=200)


# Lets Calculate an Effective Rating
min_rating = medicine['rating'].min()
max_rating = medicine['rating'].max()

def scale_rating(rating):
    rating -= min_rating
    rating = rating / (max_rating - 1)
    rating *= 5
    rating = int(round(rating, 0))

    if (int(rating) == 0 or int(rating) == 1 or int(rating) == 2):
        return 0
    else:
        return 1

medicine['eff_score'] = medicine['rating'].apply(scale_rating)

# Calculate usefulness score
medicine['usefulness'] = medicine['rating'] * medicine['usefulCount'] * medicine['eff_score']

# Calculate mean usefulness score
mean_usefulness = medicine['usefulness'].mean()

medicine2 = medicine.drop_duplicates()



def recommend(condition=list(medicine2['condition'].value_counts().index)):
    top_drugs = medicine2[medicine2['condition'] == condition][['drugName', 'usefulness']].sort_values(by='usefulness',
                                                                                                       ascending=False).reset_index(
        drop=True)
    top_drugs = top_drugs.drop_duplicates(subset=['drugName'], keep='first').head(5)

    bottom_drugs = medicine2[medicine2['condition'] == condition][['drugName', 'usefulness']].sort_values(
        by='usefulness',
        ascending=True).reset_index(
        drop=True)
    bottom_drugs = bottom_drugs.drop_duplicates(subset=['drugName'], keep='first').head(5)

    print('Condition:', condition)
    print('Top drugs type:', type(top_drugs))
    print('Top drugs:\n', top_drugs)

    return top_drugs, bottom_drugs


# Get the list of unique conditions from the dataset
conditions = medicine['condition'].unique()

selected_condition_name = st.selectbox(
'Type or select the medical condition from dropdown',
conditions)



import streamlit as st

if st.button('Show Recommendation'):
    print('Selected condition:', selected_condition_name)
    top_drugs, _ = recommend(selected_condition_name)
    print('Top drugs type:', type(top_drugs))
    print('Top drugs:\n', top_drugs)

    from PIL import Image, ImageOps

    top_drugs2 = ['Drug1.jpg', 'Drug2.jpg', 'Drug3.jpg', 'Drug4.jpg', 'Drug5.jpg']
    col1, col2, col3, col4, col5 = st.columns(5)
    image_width = 150
    border_width = 10
    border_color = '#000000'

    with col1:
        image1 = Image.open(top_drugs2[0])
        image1_with_border = ImageOps.expand(image1, border=border_width, fill=border_color)
        st.image(image1_with_border, width=image_width)
        st.markdown('1. **' + top_drugs.iloc[0]['drugName'] + '**')

    with col2:
        image2 = Image.open(top_drugs2[1])
        image2_with_border = ImageOps.expand(image2, border=border_width, fill=border_color)
        st.image(image2_with_border, width=image_width)
        st.markdown('2. **' + top_drugs.iloc[1]['drugName'] + '**')

    with col3:
        image3 = Image.open(top_drugs2[2])
        image3_with_border = ImageOps.expand(image3, border=border_width, fill=border_color)
        st.image(image3_with_border, width=image_width)
        st.markdown('3. **' + top_drugs.iloc[2]['drugName'] + '**')

    with col4:
        image4 = Image.open(top_drugs2[3])
        image4_with_border = ImageOps.expand(image4, border=border_width, fill=border_color)
        st.image(image4_with_border, width=image_width)
        st.markdown('4. **' + top_drugs.iloc[3]['drugName'] + '**')

    with col5:
        image5 = Image.open(top_drugs2[4])
        image5_with_border = ImageOps.expand(image5, border=border_width, fill=border_color)
        st.image(image5_with_border, width=image_width)
        st.markdown('5. **' + top_drugs.iloc[4]['drugName'] + '**')


    # Display top 5 drugs and their useful count
    top_drugs_df = top_drugs.reset_index(drop=True)
    top_drugs_chart = alt.Chart(top_drugs_df).mark_bar().encode(
        x=alt.X('usefulness:Q', title='Useful Count'),
        y=alt.Y('drugName:N', title='Drug Name', sort='-x'),
        tooltip=['drugName', 'usefulness']
    ).properties(title={
            "text": f'Top 5 Drugs for {selected_condition_name}',
            "fontSize": 24,
            'color': 'Neon Blue',
            'font':'Helvetica',
            "fontWeight": "bold",
            "anchor": "middle"
             },
                 width=200,  # set the width of the chart to 400 pixels
                 height=500  # set the height of the chart to 200 pixels
                 )

    st.altair_chart(top_drugs_chart, use_container_width=True)

from PIL import Image, ImageOps
if st.button('EDA and Sentiment Analysis of Dataset'):
    st.title("Sentiment Analysis")
    image1 = Image.open('sentiment_pie_chart.png')
    st.image(image1, caption='PIE Chart displays sentiment reviews of users')
    image2 = Image.open('sentiment2.png')
    st.image(image2, caption='Correlation Between Sentiment and Rating')
    image3 = Image.open('Sentiment.png')
    st.image(image3, caption='Line Chart displays positive, Negative and Neutral reviews aboubt recommended medicines')
    image4 = Image.open('SEntiment_FeatureIMP.png')
    st.image(image2, caption='Feature Importance plot using LGBM')

    st.title("Exploratory Data Analysis")
    image5 = Image.open('eda1.png')
    st.image(image5, caption='Most popular medicines from dataset')
    image6 = Image.open('eda2.png')
    st.image(image6, caption='Most High Rated medicines')
    image7 = Image.open('eda3.png')
    st.image(image7, caption='Top 10 and bottom 10 significant medicines')
    image8 = Image.open('eda4.png')
    st.image(image8, caption='Top Medicine conditions with highest reviews')
    image9 = Image.open('eda6.png')
    st.image(image9, caption='Number of Drugs per condition')
    image10 = Image.open('eda8.png')
    st.image(image10, caption='Most popular medicines per useful count')
    image11 = Image.open('eda5.png')
    st.image(image11, caption='Average Rating of medicines')


def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    if polarity > 0:
        return "positive", polarity, subjectivity
    elif polarity == 0:
        return "neutral", polarity, subjectivity
    else:
        return "negative", polarity, subjectivity


st.title("Add reviews to get Sentiment")

text = st.text_area("Enter some text")

if st.button("Analyze"):
    words = text.split()
    top = {}
    for word in words:
        if word in top:
            top[word] += 1
        else:
            top[word] = 1

    top_sorted = sorted(top.items(), key=lambda x: x[1], reverse=True)[:50]

    st.markdown("## Top Words")
    for word, frequency in top_sorted:
        st.markdown(f"- **{word}**: {frequency}")

    sentiment, polarity, subjectivity = analyze_sentiment(text)

    st.markdown("## Sentiment Analysis")
    st.markdown(f"- **Sentiment**: {sentiment.capitalize()}")
    st.markdown(f"- **Polarity**: {polarity}")
    st.markdown(f"- **Subjectivity**: {subjectivity}")
