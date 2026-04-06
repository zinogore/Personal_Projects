# Responses
def handle_response(text):
    """
    If/Else responses to messages with keywords
    """
    processed_text = text.lower()

    if 'alvin' and 'cholesterol' in processed_text:
        return 'Alvin, please take note of your cholesterol level...'
    
    if 'alvin' and 'good job' in processed_text:
        return 'Great job keeping your cholesterol level in check Alvin!'

    if 'elin' and 'cool' in processed_text:
        return '...'
    
    return 'I do not understand what you are saying...'
