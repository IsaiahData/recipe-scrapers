from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string


class AllRecipes(AbstractScraper):

    @classmethod
    def host(self):
        return 'allrecipes.com'

    def title(self):
        return self.soup.find('h1').get_text()

    def total_time(self):
        return get_minutes(self.soup.find(
            'span',
            {'class': 'ready-in-time'})
        )

    def ingredients(self):
        ingredients = self.soup.findAll(
            'li',
            {'class': "checkList__line"}
        )

        return [
            normalize_string(ingredient.get_text())
            for ingredient in ingredients
            if ingredient.get_text(strip=True) not in (
                'Add all ingredients to list',
                '',
                'ADVERTISEMENT'
            )
        ]

    def instructions(self):
        instructions = self.soup.findAll(
            'span',
            {'class': 'recipe-directions__list--item'}
        )

        return '\n'.join([
            normalize_string(instruction.get_text())
            for instruction in instructions
        ]
    
    def rating(self):                     # Added by IsaiahData on 2018-10-16
        rating = self.soup.find_all('div', {'class': 'rating-stars'})[0]['data-ratingstars']
        return rating
            
    def num_ratings(self):                # Added by IsaiahData on 2018-10-16
        num_ratings = self.soup.find_all('h4', {'class': 'helpful-header'})[0].get_text()[:-8]
        return num_ratings