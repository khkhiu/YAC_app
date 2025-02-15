# tests/test_prompts.py

import pytest
from src.bot.prompts import (
    get_random_prompt,
    get_categorical_prompt,
    PROMPTS,
    PROMPT_CATEGORIES
)

def test_get_random_prompt():
    """Test random prompt selection"""
    # Get multiple prompts to test randomness
    prompts = [get_random_prompt() for _ in range(5)]
    
    # Verify each prompt is from the main collection
    for prompt in prompts:
        assert prompt in PROMPTS
    
    # Verify we get different prompts (this could theoretically fail but is very unlikely)
    assert len(set(prompts)) > 1, "Multiple calls should return different prompts"

def test_get_categorical_prompt_valid_category():
    """Test getting prompt from a valid category"""
    # Test each category
    for category in PROMPT_CATEGORIES.keys():
        prompt = get_categorical_prompt(category)
        assert prompt in PROMPT_CATEGORIES[category]

def test_get_categorical_prompt_invalid_category():
    """Test getting prompt with invalid category"""
    prompt = get_categorical_prompt("invalid_category")
    # Should fall back to general prompts
    assert prompt in PROMPTS

def test_prompt_content():
    """Test the content quality of prompts"""
    # Test main prompts
    for prompt in PROMPTS:
        assert isinstance(prompt, str)
        assert len(prompt) > 10  # Ensure minimum length
        assert "?" in prompt  # Each prompt should be a question
    
    # Test categorical prompts
    for category, prompts in PROMPT_CATEGORIES.items():
        for prompt in prompts:
            assert isinstance(prompt, str)
            assert len(prompt) > 10
            assert "?" in prompt

def test_prompt_uniqueness():
    """Test that all prompts are unique"""
    # Check main prompts
    assert len(PROMPTS) == len(set(PROMPTS)), "Duplicate prompts found in main collection"
    
    # Check categorical prompts
    for category, prompts in PROMPT_CATEGORIES.items():
        assert len(prompts) == len(set(prompts)), f"Duplicate prompts found in {category} category"

def test_categorical_prompt_consistency():
    """Test consistency of categorical prompt retrieval"""
    category = "self_reflection"
    # Get multiple prompts from the same category
    prompts = [get_categorical_prompt(category) for _ in range(5)]
    
    # Verify all prompts are from the requested category
    for prompt in prompts:
        assert prompt in PROMPT_CATEGORIES[category]

@pytest.mark.parametrize("category", list(PROMPT_CATEGORIES.keys()))
def test_all_categories(category):
    """Test each category individually"""
    prompt = get_categorical_prompt(category)
    assert prompt in PROMPT_CATEGORIES[category]
    assert isinstance(prompt, str)
    assert len(prompt) > 10