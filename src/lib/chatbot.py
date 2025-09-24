from typing import List, Optional
from src.models.shop import Shop
from src.models.product import Product
from src.models.chat import ChatMessage
import json


def generate_shop_system_prompt(
    shop: Shop,
    products: List[Product],
    chat_history: Optional[List[ChatMessage]] = None,
    current_message: Optional[str] = None,
) -> str:
    """
    Generate a system prompt for a chatbot based on shop, product information, and chat context.

    Args:
        shop: Shop object containing shop details
        products: List of Product objects belonging to the shop
        chat_history: Optional list of previous ChatMessage objects for context
        current_message: Optional current user message being processed

    Returns:
        str: Formatted system prompt for the chatbot
    """

    # Parse tags if they exist
    tags_info = ""
    if shop.tags:
        try:
            tags_data = json.loads(shop.tags)
            if isinstance(tags_data, list):
                tags_info = f"Tags: {', '.join(tags_data)}"
            elif isinstance(tags_data, dict):
                tags_info = (
                    f"Tags: {', '.join([f'{k}: {v}' for k, v in tags_data.items()])}"
                )
            else:
                tags_info = f"Tags: {shop.tags}"
        except json.JSONDecodeError:
            tags_info = f"Tags: {shop.tags}"

    # Build shop information section
    shop_info = f"""
            Shop Name: {shop.name}
            Description: {shop.description or 'No description available'}
            {tags_info}
            Created: {shop.created_at.strftime('%Y-%m-%d')}
            Total Products: {len(products)}
            """

    # Build products information section
    products_info = "\nPRODUCTS:\n"
    if products:
        for i, product in enumerate(products, 1):
            products_info += f"""
                {i}. {product.name}
                - Description: {product.description}
                - Price: ${product.price:.2f}
                - Product ID: {product.id}
                """
    else:
        products_info += "No products available.\n"

    # Build price range information
    if products:
        prices = [p.price for p in products]
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)

        price_info = f"""
            PRICE RANGE:
            - Lowest Price: ${min_price:.2f}
            - Highest Price: ${max_price:.2f}
            - Average Price: ${avg_price:.2f}
            """
    else:
        price_info = ""

    # Combine all sections into the system prompt
    system_prompt = f"""You are a helpful shopping assistant for {shop.name}.

    SHOP INFORMATION:{shop_info}{price_info}{products_info}

    INSTRUCTIONS:
    - Be friendly and helpful when answering customer questions
    - Provide accurate information about products, prices, and availability
    - If asked about products not in the catalog, politely inform the customer
    - Help customers compare products and make informed decisions
    - Answer questions about pricing, product features, and shop policies
    - If you don't have information about something, be honest about it
    - Encourage customers to ask questions about specific products or categories

    Remember: You only have information about {shop.name} and its products listed above."""

    # Add chat history context if provided
    if chat_history:
        system_prompt += f"""

    RECENT CONVERSATION HISTORY:
    """
        # Show last 5 messages for context (to avoid token limits)
        recent_messages = chat_history[-5:] if len(chat_history) > 5 else chat_history

        for msg in recent_messages:
            system_prompt += f"User: {msg.message}\n"
            if msg.response:
                system_prompt += f"Assistant: {msg.response}\n"
            system_prompt += "\n"

        system_prompt += "Use this conversation history to provide consistent and contextual responses.\n"

    # Add current message context if provided
    if current_message:
        system_prompt += f"""

    CURRENT USER MESSAGE: "{current_message}"

    Please provide a helpful, contextual response based on the shop information, product catalog, and conversation history above."""

    return system_prompt.strip()


def generate_product_comparison_prompt(
    shop: Shop, products: List[Product], category: str = None
) -> str:
    """
    Generate a system prompt focused on product comparisons.

    Args:
        shop: Shop object
        products: List of products to compare
        category: Optional category filter

    Returns:
        str: System prompt for product comparison
    """

    filtered_products = products
    if category and shop.tags:
        try:
            tags_data = json.loads(shop.tags)
            if isinstance(tags_data, dict) and tags_data.get("category") == category:
                # If category matches shop category, include all products
                pass
            elif isinstance(tags_data, list) and category in tags_data:
                # If category is in shop tags, include all products
                pass
        except:
            pass

    comparison_info = f"You are a product comparison expert for {shop.name}.\n\n"
    comparison_info += "AVAILABLE PRODUCTS FOR COMPARISON:\n"

    for product in filtered_products:
        comparison_info += f"""
            - {product.name} (${product.price:.2f})
            Description: {product.description}
            """

    comparison_info += """
            INSTRUCTIONS:
            - Help customers compare products based on features, price, and value
            - Highlight key differences and similarities between products
            - Suggest the best product for different use cases or budgets
            - Be objective and provide balanced comparisons
            - Ask clarifying questions if needed to give better recommendations"""

    return comparison_info


def generate_generic_system_prompt(
    chat_history: Optional[List[ChatMessage]] = None,
    current_message: Optional[str] = None,
    context: Optional[str] = None,
) -> str:
    """
    Generate a generic system prompt for a chatbot without shop-specific information.

    Args:
        chat_history: Optional list of previous ChatMessage objects for context
        current_message: Optional current user message being processed
        context: Optional additional context information to include

    Returns:
        str: Formatted generic system prompt for the chatbot
    """

    system_prompt = """You are a helpful and friendly AI assistant.

    INSTRUCTIONS:
    - Be friendly, helpful, and engaging in your responses
    - Provide accurate and useful information
    - Ask clarifying questions when needed
    - Be honest about what you can and cannot help with
    - Maintain a conversational and natural tone
    - If you don't know something, admit it rather than making things up"""

    # Add additional context if provided
    if context:
        system_prompt += f"""

    ADDITIONAL CONTEXT:
    {context}"""

    # Add chat history context if provided
    if chat_history:
        system_prompt += f"""

    RECENT CONVERSATION HISTORY:
    """
        # Show last 5 messages for context (to avoid token limits)
        recent_messages = chat_history[-5:] if len(chat_history) > 5 else chat_history

        for msg in recent_messages:
            system_prompt += f"User: {msg.message}\n"
            if msg.response:
                system_prompt += f"Assistant: {msg.response}\n"
            system_prompt += "\n"

        system_prompt += "Use this conversation history to provide consistent and contextual responses.\n"

    # Add current message context if provided
    if current_message:
        system_prompt += f"""

    CURRENT USER MESSAGE: "{current_message}"

    Please provide a helpful and engaging response."""

    return system_prompt.strip()


def generate_customer_support_prompt(
    chat_history: Optional[List[ChatMessage]] = None,
    current_message: Optional[str] = None,
    support_context: Optional[str] = None,
) -> str:
    """
    Generate a system prompt specifically for customer support scenarios.

    Args:
        chat_history: Optional list of previous ChatMessage objects for context
        current_message: Optional current user message being processed
        support_context: Optional support-specific context (policies, procedures, etc.)

    Returns:
        str: Formatted customer support system prompt
    """

    system_prompt = """You are a professional and empathetic customer support assistant.

INSTRUCTIONS:
- Be patient, understanding, and solution-oriented
- Listen carefully to customer concerns and acknowledge their feelings
- Provide clear, step-by-step solutions when possible
- Escalate complex issues to human representatives when appropriate
- Maintain a professional yet friendly tone
- Follow up to ensure customer satisfaction
- Be honest about limitations and timelines"""

    # Add support-specific context
    if support_context:
        system_prompt += f"""

SUPPORT CONTEXT:
{support_context}"""

    # Add chat history context if provided
    if chat_history:
        system_prompt += f"""

RECENT CONVERSATION HISTORY:
"""
        # Show last 10 messages for support context (more history needed for complex issues)
        recent_messages = chat_history[-10:] if len(chat_history) > 10 else chat_history

        for msg in recent_messages:
            system_prompt += f"User: {msg.message}\n"
            if msg.response:
                system_prompt += f"Support: {msg.response}\n"
            system_prompt += "\n"

        system_prompt += "Use this conversation history to understand the customer's issue and provide consistent support.\n"

    # Add current message context if provided
    if current_message:
        system_prompt += f"""

CURRENT CUSTOMER MESSAGE: "{current_message}"

Please provide helpful, empathetic, and solution-focused support."""

    return system_prompt.strip()
