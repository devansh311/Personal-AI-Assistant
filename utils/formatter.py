def extract_text(message):

    content = message.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        text = ""

        for part in content:

            if isinstance(part, dict):

                if part.get("type") == "text":
                    text += part.get("text", "")

            else:
                text += str(part)

        return text

    return str(content)