# Your name: Max Meston
# Your student id: 1171 2492
# Your email: mmeston@umich.edu
# List who you have worked with on this homework: Hudson Bush, Emma Moore

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # select all rows from the restaurants table
    cursor.execute("SELECT * FROM restaurants")

    # create an empty dictionary to store the restaurant data
    restaurants = {}

    # iterate through the rows returned by the query
    for row in cursor.fetchall():
        # extract the restaurant name, category, building, and rating from the row
        name = row[1]
        category_id = row[2]
        building_id = row[3]
        rating = row[4]

        # if the restaurant is not already in the dictionary, add it with an empty dictionary as the value
        if name not in restaurants:
            restaurants[name] = {}

        cursor.execute("SELECT category FROM categories WHERE id=?", (category_id,))
        category_name = cursor.fetchone()[0]
       
        cursor.execute("SELECT building FROM buildings WHERE id=?", (building_id,))
        building_name = cursor.fetchone()[0]

        # add the category, building, and rating information to the nested dictionary
        restaurants[name]['category'] = category_name
        restaurants[name]['building'] = building_name
        restaurants[name]['rating'] = rating

    conn.close()

    return restaurants


def plot_rest_categories(db):

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # select the category name and count of restaurants in each category
    cursor.execute("SELECT categories.category, COUNT(restaurants.category_id) FROM restaurants JOIN categories ON restaurants.category_id=categories.id GROUP BY categories.category")

    # create an empty dictionary to store the category counts
    category_counts = {}

    # iterate through the rows returned by the query
    for row in cursor.fetchall():
        # extract the category name and count from the row
        category_name = row[0]
        count = row[1]

        # add the category name and count to the dictionary
        category_counts[category_name] = count

    conn.close()

    category_counts = dict(sorted(category_counts.items(), key=lambda item: item[1], reverse=False))

    # plot the category counts as a bar chart
    max_count = max(category_counts.values())
    plt.barh(range(len(category_counts)), list(category_counts.values()), align='center')
    plt.yticks(range(len(category_counts)), list(category_counts.keys()))
    plt.xticks(range(0, max_count+1, 1))
    plt.ylabel('Restaurant Category')
    plt.xlabel('Number of Restaurants')
    plt.title('Resturants on South U')
    plt.show()

    return category_counts



def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # select the id of the building with the given building number
    cursor.execute("SELECT id FROM buildings WHERE building = ?", (building_num,))
    building_id = cursor.fetchone()[0]

    # select the restaurant names from the restaurants table, filter by the building_id, and sort by rating
    cursor.execute("SELECT name FROM restaurants WHERE building_id = ? ORDER BY rating DESC", (building_id,))

    # fetch all rows as a list of tuples
    rows = cursor.fetchall()

    # extract the restaurant names from the rows and convert to a list
    restaurant_names = [row[0] for row in rows]

    conn.close()

    return restaurant_names



#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():

    # (load_rest_data('South_U_Restaurants.db'))
    # plot_rest_categories('South_U_Restaurants.db')
    # print(find_rest_in_building(1140, 'South_U_Restaurants.db'))
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    # def test_get_highest_rating(self):
    #     highest_rating = get_highest_rating('South_U_Restaurants.db')
    #     self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
