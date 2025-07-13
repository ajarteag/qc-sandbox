import React, { useState } from 'react';
import styled from 'styled-components';
import { DailyEntry, Meal, Food } from '../types';
import { Plus, ArrowLeft, Edit3 } from 'lucide-react';

interface FoodDiaryProps {
  onBack: () => void;
}

const DiaryContainer = styled.div`
  max-width: 1000px;
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

const DailySection = styled.div`
  background: white;
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
`;

const DateHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
`;

const DateTitle = styled.h2`
  color: #333;
  font-size: 1.8rem;
  margin: 0;
`;

const AddMealButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-2px);
  }
`;

const MealSection = styled.div`
  background: #f8f9fa;
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 15px;
`;

const MealHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
`;

const MealTitle = styled.h3`
  color: #333;
  font-size: 1.3rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const EditButton = styled.button`
  background: #e9ecef;
  border-radius: 8px;
  padding: 8px 12px;
  color: #666;
  font-size: 0.9rem;
  transition: background 0.2s;

  &:hover {
    background: #dee2e6;
  }
`;

const FoodList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const FoodItem = styled.div`
  background: white;
  border-radius: 10px;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const FoodInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 5px;
`;

const FoodName = styled.span`
  font-weight: 600;
  color: #333;
`;

const FoodNutrition = styled.span`
  color: #666;
  font-size: 0.9rem;
`;

const NutritionSummary = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 15px;
  padding: 20px;
  margin-top: 20px;
`;

const SummaryTitle = styled.h4`
  margin: 0 0 15px 0;
  font-size: 1.2rem;
`;

const NutritionGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
`;

const NutritionItem = styled.div`
  text-align: center;
`;

const NutritionValue = styled.div`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 5px;
`;

const NutritionLabel = styled.div`
  font-size: 0.9rem;
  opacity: 0.9;
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 60px 20px;
  color: #666;
`;

const EmptyStateTitle = styled.h3`
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #333;
`;

const FoodDiary: React.FC<FoodDiaryProps> = ({ onBack }) => {
  const [dailyEntries, setDailyEntries] = useState<DailyEntry[]>([
    {
      date: '2024-07-12',
      meals: [
        {
          id: '1',
          name: 'Breakfast',
          foods: [
            {
              id: '1',
              name: 'Oatmeal with berries',
              calories: 250,
              protein: 8,
              carbs: 45,
              fat: 4,
              fiber: 6,
              sugar: 12,
              sodium: 150
            }
          ],
          totalCalories: 250,
          totalProtein: 8,
          totalCarbs: 45,
          totalFat: 4
        },
        {
          id: '2',
          name: 'Lunch',
          foods: [
            {
              id: '2',
              name: 'Grilled chicken salad',
              calories: 350,
              protein: 35,
              carbs: 15,
              fat: 12,
              fiber: 8,
              sugar: 5,
              sodium: 400
            }
          ],
          totalCalories: 350,
          totalProtein: 35,
          totalCarbs: 15,
          totalFat: 12
        }
      ],
      totalCalories: 600,
      totalProtein: 43,
      totalCarbs: 60,
      totalFat: 16
    }
  ]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const calculateDailyTotals = (entry: DailyEntry) => {
    return {
      calories: entry.meals.reduce((sum, meal) => sum + meal.totalCalories, 0),
      protein: entry.meals.reduce((sum, meal) => sum + meal.totalProtein, 0),
      carbs: entry.meals.reduce((sum, meal) => sum + meal.totalCarbs, 0),
      fat: entry.meals.reduce((sum, meal) => sum + meal.totalFat, 0)
    };
  };

  return (
    <DiaryContainer>
      <Header>
        <BackButton onClick={onBack}>
          <ArrowLeft size={24} />
        </BackButton>
        <Title>My Food Diary</Title>
      </Header>

      {dailyEntries.length === 0 ? (
        <EmptyState>
          <EmptyStateTitle>No entries yet</EmptyStateTitle>
          <p>Start tracking your meals by adding your first entry!</p>
        </EmptyState>
      ) : (
        dailyEntries.map((entry) => {
          const totals = calculateDailyTotals(entry);
          
          return (
            <DailySection key={entry.date}>
              <DateHeader>
                <DateTitle>{formatDate(entry.date)}</DateTitle>
                <AddMealButton>
                  <Plus size={16} />
                  Add Meal
                </AddMealButton>
              </DateHeader>

              {entry.meals.map((meal) => (
                <MealSection key={meal.id}>
                  <MealHeader>
                    <MealTitle>
                      {meal.name}
                      <EditButton>
                        <Edit3 size={14} />
                      </EditButton>
                    </MealTitle>
                  </MealHeader>

                  <FoodList>
                    {meal.foods.map((food) => (
                      <FoodItem key={food.id}>
                        <FoodInfo>
                          <FoodName>{food.name}</FoodName>
                          <FoodNutrition>
                            {food.calories} cal • {food.protein}g protein • {food.carbs}g carbs • {food.fat}g fat
                          </FoodNutrition>
                        </FoodInfo>
                      </FoodItem>
                    ))}
                  </FoodList>
                </MealSection>
              ))}

              <NutritionSummary>
                <SummaryTitle>Daily Summary</SummaryTitle>
                <NutritionGrid>
                  <NutritionItem>
                    <NutritionValue>{totals.calories}</NutritionValue>
                    <NutritionLabel>Calories</NutritionLabel>
                  </NutritionItem>
                  <NutritionItem>
                    <NutritionValue>{totals.protein}g</NutritionValue>
                    <NutritionLabel>Protein</NutritionLabel>
                  </NutritionItem>
                  <NutritionItem>
                    <NutritionValue>{totals.carbs}g</NutritionValue>
                    <NutritionLabel>Carbs</NutritionLabel>
                  </NutritionItem>
                  <NutritionItem>
                    <NutritionValue>{totals.fat}g</NutritionValue>
                    <NutritionLabel>Fat</NutritionLabel>
                  </NutritionItem>
                </NutritionGrid>
              </NutritionSummary>
            </DailySection>
          );
        })
      )}
    </DiaryContainer>
  );
};

export default FoodDiary; 