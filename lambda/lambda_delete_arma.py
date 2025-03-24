import json
import boto3

dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('InventarioArmas')

def lambda_handler(event, context):
    print("DEBUG EVENT:", json.dumps(event))

    try:
        arma_id = event['pathParameters']['id'].strip()

        existente = tabla.get_item(Key={'arma_id': arma_id})

        if 'Item' not in existente:
            return {
                'statusCode': 404,
                'body': json.dumps({'mensaje': 'Arma no encontrada'}),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

        tabla.delete_item(Key={'arma_id': arma_id})

        return {
            'statusCode': 200,
            'body': json.dumps({'mensaje': 'Arma eliminada exitosamente'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }