import React, { useState } from 'react';
import styled from 'styled-components';
import { User, Avatar } from '../types';

interface OnboardingProps {
  onComplete: (user: User) => void;
}

const OnboardingContainer = styled.div`
  max-width: 600px;
  margin: 50px auto;
  padding: 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h1`
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 2.5rem;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const Label = styled.label`
  font-weight: 600;
  color: #555;
  font-size: 1.1rem;
`;

const Input = styled.input`
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  font-size: 1rem;
  transition: border-color 0.3s;

  &:focus {
    border-color: #667eea;
  }
`;

const Select = styled.select`
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  font-size: 1rem;
  background: white;
  transition: border-color 0.3s;

  &:focus {
    border-color: #667eea;
  }
`;

const Button = styled.button`
  padding: 15px 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-2px);
  }
`;

const AvatarSection = styled.div`
  margin-top: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 15px;
`;

const AvatarPreview = styled.div`
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #ddd;
  margin: 0 auto 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  border: 4px solid #667eea;
`;

const AvatarOptions = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-top: 20px;
`;

const OptionGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const ColorOption = styled.div<{ color: string; selected: boolean }>`
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: ${props => props.color};
  cursor: pointer;
  border: 3px solid ${props => props.selected ? '#667eea' : 'transparent'};
  transition: transform 0.2s;

  &:hover {
    transform: scale(1.1);
  }
`;

const Onboarding: React.FC<OnboardingProps> = ({ onComplete }) => {
  const [step, setStep] = useState(1);
  const [userData, setUserData] = useState({
    name: '',
    age: '',
    gender: '',
    height: '',
    weight: '',
    goal: ''
  });

  const [avatar, setAvatar] = useState<Avatar>({
    hairColor: '#8B4513',
    hairStyle: 'short',
    eyeColor: '#000000',
    skinTone: '#FFDBB4',
    accessories: []
  });

  const handleInputChange = (field: string, value: string) => {
    setUserData(prev => ({ ...prev, [field]: value }));
  };

  const handleAvatarChange = (field: keyof Avatar, value: string | string[]) => {
    setAvatar(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (step === 1) {
      setStep(2);
    } else {
      const user: User = {
        name: userData.name,
        age: parseInt(userData.age),
        gender: userData.gender as 'male' | 'female' | 'other',
        height: parseInt(userData.height),
        weight: parseInt(userData.weight),
        goal: userData.goal as 'bulk' | 'cut' | 'track',
        avatar
      };
      onComplete(user);
    }
  };

  const hairColors = ['#8B4513', '#654321', '#A0522D', '#CD853F', '#DEB887', '#F5DEB3'];
  const eyeColors = ['#000000', '#8B4513', '#0066CC', '#228B22', '#8B008B'];
  const skinTones = ['#FFDBB4', '#EDB98A', '#D08B5B', '#AE5D29', '#8D4A43'];

  return (
    <OnboardingContainer>
      <Title>{step === 1 ? 'Welcome to Nutrition Tracker!' : 'Create Your Avatar'}</Title>
      
      <Form onSubmit={handleSubmit}>
        {step === 1 ? (
          <>
            <FormGroup>
              <Label>Name</Label>
              <Input
                type="text"
                value={userData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                required
                placeholder="Enter your name"
              />
            </FormGroup>

            <FormGroup>
              <Label>Age</Label>
              <Input
                type="number"
                value={userData.age}
                onChange={(e) => handleInputChange('age', e.target.value)}
                required
                placeholder="Enter your age"
                min="1"
                max="120"
              />
            </FormGroup>

            <FormGroup>
              <Label>Gender</Label>
              <Select
                value={userData.gender}
                onChange={(e) => handleInputChange('gender', e.target.value)}
                required
              >
                <option value="">Select gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </Select>
            </FormGroup>

            <FormGroup>
              <Label>Height (cm)</Label>
              <Input
                type="number"
                value={userData.height}
                onChange={(e) => handleInputChange('height', e.target.value)}
                required
                placeholder="Enter your height in cm"
                min="100"
                max="250"
              />
            </FormGroup>

            <FormGroup>
              <Label>Weight (kg)</Label>
              <Input
                type="number"
                value={userData.weight}
                onChange={(e) => handleInputChange('weight', e.target.value)}
                required
                placeholder="Enter your weight in kg"
                min="30"
                max="300"
              />
            </FormGroup>

            <FormGroup>
              <Label>Goal</Label>
              <Select
                value={userData.goal}
                onChange={(e) => handleInputChange('goal', e.target.value)}
                required
              >
                <option value="">Select your goal</option>
                <option value="bulk">I want to bulk</option>
                <option value="cut">I want to cut</option>
                <option value="track">I want to track my nutrients</option>
              </Select>
            </FormGroup>
          </>
        ) : (
          <AvatarSection>
            <AvatarPreview>
              👤
            </AvatarPreview>
            
            <AvatarOptions>
              <OptionGroup>
                <Label>Hair Color</Label>
                <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                  {hairColors.map(color => (
                    <ColorOption
                      key={color}
                      color={color}
                      selected={avatar.hairColor === color}
                      onClick={() => handleAvatarChange('hairColor', color)}
                    />
                  ))}
                </div>
              </OptionGroup>

              <OptionGroup>
                <Label>Eye Color</Label>
                <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                  {eyeColors.map(color => (
                    <ColorOption
                      key={color}
                      color={color}
                      selected={avatar.eyeColor === color}
                      onClick={() => handleAvatarChange('eyeColor', color)}
                    />
                  ))}
                </div>
              </OptionGroup>

              <OptionGroup>
                <Label>Skin Tone</Label>
                <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                  {skinTones.map(color => (
                    <ColorOption
                      key={color}
                      color={color}
                      selected={avatar.skinTone === color}
                      onClick={() => handleAvatarChange('skinTone', color)}
                    />
                  ))}
                </div>
              </OptionGroup>
            </AvatarOptions>
          </AvatarSection>
        )}

        <Button type="submit">
          {step === 1 ? 'Next: Create Avatar' : 'Complete Setup'}
        </Button>
      </Form>
    </OnboardingContainer>
  );
};

export default Onboarding; 