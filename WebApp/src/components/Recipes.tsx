import React, { useState } from 'react';
import styled from 'styled-components';
import { Recipe } from '../types';
import { ArrowLeft, Plus, Clock, Users, ChefHat, Heart } from 'lucide-react';

interface RecipesProps {
  onBack: () => void;
  type: 'personal' | 'friends';
}

const RecipesContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
`;

const BackButton = styled.button`
  background: white;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;

  &:hover {
    transform: scale(1.1);
  }
`;

const Title = styled.h1`
  color: white;
  font-size: 2.5rem;
  margin: 0;
`;

const AddButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 15px;
  padding: 15px 25px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: transform 0.2s;
  margin-left: auto;

  &:hover {
    transform: translateY(-2px);
  }
`;

const RecipesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
`;

const RecipeCard = styled.div`
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;

  &:hover {
    transform: translateY(-5px);
  }
`;

const RecipeImage = styled.div`
  height: 200px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 3rem;
`;

const RecipeContent = styled.div`
  padding: 25px;
`;

const RecipeTitle = styled.h3`
  color: #333;
  font-size: 1.4rem;
  margin: 0 0 10px 0;
  font-weight: 600;
`;

const RecipeMeta = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
  color: #666;
  font-size: 0.9rem;
`;

const MetaItem = styled.div`
  display: flex;
  align-items: center;
  gap: 5px;
`;

const RecipeDescription = styled.p`
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
`;

const RecipeStats = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
`;

const NutritionInfo = styled.div`
  display: flex;
  gap: 15px;
  font-size: 0.9rem;
  color: #666;
`;

const NutritionItem = styled.span`
  font-weight: 600;
  color: #333;
`;

const LikeButton = styled.button`
  background: #f8f9fa;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  transition: all 0.2s;

  &:hover {
    background: #e9ecef;
    color: #dc3545;
  }

  &.liked {
    background: #dc3545;
    color: white;
  }
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 80px 20px;
  color: #666;
`;

const EmptyStateIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.5;
`;

const EmptyStateTitle = styled.h3`
  font-size: 1.8rem;
  margin-bottom: 10px;
  color: #333;
`;

const EmptyStateText = styled.p`
  font-size: 1.1rem;
  margin-bottom: 30px;
`;

const Recipes: React.FC<RecipesProps> = ({ onBack, type }) => {
  const [recipes, setRecipes] = useState<Recipe[]>([
    {
      id: '1',
      name: 'Protein Power Bowl',
      ingredients: [
        {
          id: '1',
          name: 'Quinoa',
          calories: 120,
          protein: 4,
          carbs: 22,
          fat: 2,
          fiber: 3,
          sugar: 1,
          sodium: 10
        },
        {
          id: '2',
          name: 'Grilled Chicken',
          calories: 165,
          protein: 31,
          carbs: 0,
          fat: 3.6,
          fiber: 0,
          sugar: 0,
          sodium: 74
        }
      ],
      instructions: [
        'Cook quinoa according to package instructions',
        'Grill chicken breast until cooked through',
        'Combine with vegetables and serve'
      ],
      prepTime: 15,
      cookTime: 20,
      servings: 2,
      isPersonal: type === 'personal',
      author: type === 'friends' ? 'Sarah Johnson' : undefined
    },
    {
      id: '2',
      name: 'Berry Smoothie Bowl',
      ingredients: [
        {
          id: '3',
          name: 'Mixed Berries',
          calories: 85,
          protein: 1,
          carbs: 21,
          fat: 0.5,
          fiber: 4,
          sugar: 15,
          sodium: 1
        }
      ],
      instructions: [
        'Blend frozen berries with yogurt',
        'Top with granola and fresh fruit',
        'Serve immediately'
      ],
      prepTime: 10,
      cookTime: 0,
      servings: 1,
      isPersonal: type === 'personal',
      author: type === 'friends' ? 'Mike Chen' : undefined
    }
  ]);

  const [likedRecipes, setLikedRecipes] = useState<Set<string>>(new Set());

  const toggleLike = (recipeId: string) => {
    const newLiked = new Set(likedRecipes);
    if (newLiked.has(recipeId)) {
      newLiked.delete(recipeId);
    } else {
      newLiked.add(recipeId);
    }
    setLikedRecipes(newLiked);
  };

  const calculateTotalNutrition = (recipe: Recipe) => {
    return recipe.ingredients.reduce(
      (total, ingredient) => ({
        calories: total.calories + ingredient.calories,
        protein: total.protein + ingredient.protein,
        carbs: total.carbs + ingredient.carbs,
        fat: total.fat + ingredient.fat
      }),
      { calories: 0, protein: 0, carbs: 0, fat: 0 }
    );
  };

  return (
    <RecipesContainer>
      <Header>
        <BackButton onClick={onBack}>
          <ArrowLeft size={24} />
        </BackButton>
        <Title>
          {type === 'personal' ? 'Personal Recipes' : "Friends' Recipes"}
        </Title>
        {type === 'personal' && (
          <AddButton>
            <Plus size={20} />
            Add Recipe
          </AddButton>
        )}
      </Header>

      {recipes.length === 0 ? (
        <EmptyState>
          <EmptyStateIcon>
            {type === 'personal' ? <ChefHat size={80} /> : <Users size={80} />}
          </EmptyStateIcon>
          <EmptyStateTitle>
            {type === 'personal' ? 'No personal recipes yet' : 'No friends recipes yet'}
          </EmptyStateTitle>
          <EmptyStateText>
            {type === 'personal' 
              ? 'Start building your recipe collection by adding your favorite dishes!'
              : 'Your friends haven\'t shared any recipes yet. Check back later!'
            }
          </EmptyStateText>
        </EmptyState>
      ) : (
        <RecipesGrid>
          {recipes.map((recipe) => {
            const nutrition = calculateTotalNutrition(recipe);
            
            return (
              <RecipeCard key={recipe.id}>
                <RecipeImage>
                  🍽️
                </RecipeImage>
                <RecipeContent>
                  <RecipeTitle>{recipe.name}</RecipeTitle>
                  
                  <RecipeMeta>
                    <MetaItem>
                      <Clock size={16} />
                      {recipe.prepTime + recipe.cookTime} min
                    </MetaItem>
                    <MetaItem>
                      <Users size={16} />
                      {recipe.servings} servings
                    </MetaItem>
                    {recipe.author && (
                      <MetaItem>
                        <ChefHat size={16} />
                        {recipe.author}
                      </MetaItem>
                    )}
                  </RecipeMeta>

                  <RecipeDescription>
                    A delicious and nutritious recipe perfect for your health goals.
                  </RecipeDescription>

                  <RecipeStats>
                    <NutritionInfo>
                      <span><NutritionItem>{nutrition.calories}</NutritionItem> cal</span>
                      <span><NutritionItem>{nutrition.protein}g</NutritionItem> protein</span>
                      <span><NutritionItem>{nutrition.carbs}g</NutritionItem> carbs</span>
                    </NutritionInfo>
                    
                    <LikeButton
                      className={likedRecipes.has(recipe.id) ? 'liked' : ''}
                      onClick={() => toggleLike(recipe.id)}
                    >
                      <Heart size={18} />
                    </LikeButton>
                  </RecipeStats>
                </RecipeContent>
              </RecipeCard>
            );
          })}
        </RecipesGrid>
      )}
    </RecipesContainer>
  );
};

export default Recipes; 