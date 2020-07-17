import boto3

textract = boto3.client('textract')


def extract(filePath: str, analyze: bool = False):
    with open(filePath, 'rb') as document:
        imageBytes = bytearray(document.read())

    response = textract.analyze_document(
        Document={'Bytes': imageBytes},
        FeatureTypes=['FORMS']
    ) if analyze else textract.detect_document_text(
        Document={'Bytes': imageBytes},
    )

    count = 0
    confidence = 0
    textLines = []

    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            count += 1
            confidence += block['Confidence']
            textLines.append(block['Text'])

    averageConfidence = confidence / count

    # print(textLines)
    # print(count)
    # print(confidence)
    # print(averageConfidence)

    joined: str = ' '.join(textLines)

    return joined, textLines, averageConfidence, response


if __name__ == '__main__':
    extract('../util/resources/arturo.jpg')

'''
def main():
    document = 'arturo.jpg'
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket,
                'Name': document
            }
        })

    parsedData = [item['Text'] for item in response['Blocks'] if 'Text' in item]
    joined: str = ' '.join(parsedData)

    print(joined)
    print(genObject(joined))


if __name__ == "__main__":
    main()
'''
