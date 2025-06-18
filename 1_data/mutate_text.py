import random
from typing import List, Callable, Tuple

def get_random_words(text: str, num_words: int) -> List[str]:
    """Get random words from the text."""
    words = text.split()
    if len(words) <= num_words:
        return words
    return random.sample(words, num_words)

def deletion(words: List[str], start_idx: int, length: int) -> List[str]:
    """Delete N words starting from start_idx."""
    return words[:start_idx] + words[start_idx + length:]

def duplication(words: List[str], start_idx: int, length: int) -> List[str]:
    """Duplicate N words starting from start_idx."""
    return words[:start_idx + length] + words[start_idx:start_idx + length] + words[start_idx + length:]

def inversion(words: List[str], start_idx: int, length: int) -> List[str]:
    """Invert N words starting from start_idx."""
    return words[:start_idx] + words[start_idx:start_idx + length][::-1] + words[start_idx + length:]

def insertion(words: List[str], start_idx: int, length: int) -> List[str]:
    """Insert N random words from the text at start_idx."""
    random_words = get_random_words(" ".join(words), length)
    return words[:start_idx] + random_words + words[start_idx:]

def substitution(words: List[str], start_idx: int, length: int) -> List[str]:
    """Substitute N words starting from start_idx with random words from the text."""
    random_words = get_random_words(" ".join(words), length)
    return words[:start_idx] + random_words + words[start_idx + length:]

def translocation(words: List[str], start_idx: int, length: int) -> List[str]:
    """Move N words starting from start_idx to a random position."""
    if len(words) <= length:
        return words
    
    # Get the words to move
    words_to_move = words[start_idx:start_idx + length]
    # Remove the words from their original position
    remaining_words = words[:start_idx] + words[start_idx + length:]
    # Choose a new position
    new_pos = random.randint(0, len(remaining_words))
    # Insert the words at the new position
    return remaining_words[:new_pos] + words_to_move + remaining_words[new_pos:]

def get_mutation_functions() -> List[Callable[[List[str], int, int], List[str]]]:
    """Return a list of all mutation functions."""
    return [
        deletion,
        duplication,
        inversion,
        insertion,
        substitution,
        translocation
    ]

Far out in the uncharted backwaters of the unfashionable  end  of the  western  spiral  arm  of  the Galaxy lies a small unregarded yellow sun.

def mutate_text(text: str, mutation_rate: float = 0.05) -> str:
    """Apply mutations to the text word by word."""
    words = text.split()
    if len(words) <= 1:
        return text
    
    i = 0
    while i < len(words):
        if random.random() < mutation_rate:
            # Randomly choose mutation length (1 to 5)
            mutation_length = random.randint(1, min(5, len(words) - i))
            # Choose a random mutation type
            mutation = random.choice(get_mutation_functions())
            # Apply the mutation
            words = mutation(words, i, mutation_length)
            # Skip the mutated words
            i += mutation_length
        else:
            i += 1
    
    return " ".join(words) 