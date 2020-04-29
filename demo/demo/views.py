from django.http import JsonResponse
from django.views import View


class PetListView(View):
    def get(self, request):
        '''
        select all pets from database and return them as response
        --api-doc--
        summary: List all pets
        operationId: listPets
        tags:
          - pets
        parameters:
          - name: limit
            in: query
            description: How many items to return at one time (max 100)
            required: false
            schema:
              type: integer
              format: int32
        responses:
          '200':
            description: A paged array of pets
            headers:
              x-next:
                description: A link to the next page of responses
                schema:
                  type: string
            content:
              application/json:
                schema:
                  $ref: "#/components/schemas/Pets"
          default:
            description: unexpected error
            content:
              application/json:
                schema:
                  $ref: "#/components/schemas/Error"
        '''
        content = {
            'asd': '123'
        }
        return JsonResponse(content)

    def post(self, request):
        '''
        --api-doc--
        summary: Create a pet
        operationId: createPets
        tags:
          - pets
        responses:
          '201':
            description: Null response
          default:
            description: unexpected error
            content:
              application/json:
                schema:
                  $ref: "#/components/schemas/Error"
        '''
        return HttpResponse('create pet')



class PetView(View):
    '''
    here can store common doc like path paramerters
    --api-doc--
    parameters:
      - name: pet_id
        in: path
        required: true
        description: The id of the pet to retrieve
        schema:
          type: string
    '''

    def get(self, request, pet_id=None):
        '''
        --api-doc--
        summary: Info for a specific pet
        operationId: showPetById
        tags:
          - pets
        responses:
          '200':
            description: Expected response to a valid request
            content:
              application/json:
                schema:
                  $ref: "#/components/schemas/Pet"
          default:
            description: unexpected error
            content:
              application/json:
                schema:
                  $ref: "#/components/schemas/Error"
        '''
        content = {
            'id': 1,
            'name': 'peter',
            'tag': 'dog'
        }
        return JsonResponse(content)
