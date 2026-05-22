from django.test import TestCase
from django.urls import reverse
from .models import Recipe, Category


class MainViewTest(TestCase):

    
    def test_main_uses_correct_template(self):
        response = self.client.get(reverse('main'))
        self.assertTemplateUsed(response, 'main.html')

    def test_main_returns_last_5_recipes(self):
        category = Category.objects.create(name='Test')
        for i in range(6):
            Recipe.objects.create(
                title=f'Recipe {i}',
                description='desc',
                instructions='instr',
                ingredients='ingr',
                category=category
            )
        response = self.client.get(reverse('main'))
        self.assertEqual(len(response.context['recipes']), 5)

    def test_main_empty_recipes(self):
        response = self.client.get(reverse('main'))
        self.assertContains(response, 'No recipes found.')


class CategoryListViewTest(TestCase):

    def test_category_list_returns_200(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)

    def test_category_list_uses_correct_template(self):
        response = self.client.get(reverse('category_list'))
        self.assertTemplateUsed(response, 'category_list.html')

    def test_category_list_shows_categories(self):
        Category.objects.create(name='Breakfast')
        Category.objects.create(name='Dinner')
        response = self.client.get(reverse('category_list'))
        self.assertEqual(len(response.context['categories']), 2)

    def test_category_list_empty(self):
        response = self.client.get(reverse('category_list'))
        self.assertContains(response, 'No categories found.')