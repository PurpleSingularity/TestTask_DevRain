# Examples of use
Below are examples of raw answers from the model, as indicated in the task.

## Example 1: Cooking instruction

**app**: What should i do? 
    Type "C" - for cooking instructions. 
    Type "I" - for ingredients. 
    Type "S" - for stop.

**user**: c

**app**: Generate cooking instructions for: 

**user**: creamy corn

**app**: {'title': 'Creamy Corn', 'error': None, 'recipe': ['1. Preparation:
Ensure all ingredients are measured and ready for use. If using frozen corn,
it is recommended to thaw it slightly before cooking to ensure even heating.',
'2. Melt Butter: In a large skillet or saucepan, melt 2 tablespoons
(approximately 28 grams) of unsalted butter over medium heat.', '3. Add Corn:
Add 4 cups (approximately 600-700 grams) of corn kernels to the skillet. You may
use fresh, frozen, or canned corn. If using canned corn, drain it thoroughly
before adding. Sauté the corn for 3-5 minutes, stirring occasionally, until it
is heated through and slightly tender.', '4. Incorporate Cream Cheese and Liquids:
Reduce the heat to low. Add 4 ounces (approximately 113 grams) of cream cheese, cut
into cubes, to the skillet. Pour in 1/4 cup (approximately 60 milliliters) of
whole milk or heavy cream. Stir continuously until the cream cheese is fully
melted and incorporated, creating a smooth, creamy sauce.', '5. Seasoning: Stir
in 1-2 teaspoons of granulated sugar (adjust to desired sweetness, as corn
sweetness varies), 1/2 teaspoon of salt, and 1/4 teaspoon of black pepper.
Taste and adjust seasonings as necessary. For enhanced flavor, a pinch of
cayenne pepper or a dash of garlic powder may be added.', '6. Simmer and
Thicken: Continue to simmer the creamy corn mixture over low heat for an
additional 5-7 minutes, stirring occasionally, until the sauce has thickened
to your desired consistency. Avoid boiling to prevent the sauce from separating.
', '7. Serve: Remove from heat and serve immediately as a side dish. Garnish
with fresh chopped chives or parsley, if desired.'], 'ingredients': None,
'is_done': True}


## Example 2: Ingredients

**app**: What should i do? 
    Type "C" - for cooking instructions. 
    Type "I" - for ingredients. 
    Type "S" - for stop.

**user**: i

**app**: Generate required ingredients for: 

**user**: {'title': None, 'error': "The recipe provided is too general. /
To provide accurate ingredients, please specify a particular chicken dish /
(e.g., 'Roast Chicken', 'Chicken Curry', 'Chicken Stir-fry').", 'recipe': /
None, 'ingredients': None, 'is_done': False}

**user**: i

**app**: Generate required ingredients for: 

**user**: Roast Chicken

**app**: {'title': 'Roast Chicken', 'error': None, 'recipe': None, 'ingredients': ['1. Whole Chicken: 1 (approximately 3-4 pounds or 1.4-1.8 kg), giblets removed', '2. Olive Oil: 2-3 tablespoons', '3. Kosher Salt: 1-2 tablespoons, or to taste (adjust based on chicken size and preference)', '4. Black Pepper: 1 teaspoon, freshly ground, or to taste', '5. Fresh Rosemary: 3-4 sprigs', '6. Fresh Thyme: 5-6 sprigs', '7. Lemon: 1, halved (optional, for stuffing the cavity)', '8. Onion: 1 small, quartered (optional, for stuffing the cavity or roasting alongside)', '9. Garlic: 4-6 cloves, smashed (optional, for stuffing the cavity or roasting alongside)', '10. Unsalted Butter: 2 tablespoons, melted (optional, for basting or rubbing under the skin)'], 'is_done': True}