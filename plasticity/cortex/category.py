from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from plasticity.base.endpoint import Endpoint


class Category(Endpoint):
    """The Category Endpoint identifies the category of a word. 

    Noe: this a temporary class for working on babi tasks.
    """
    def __init__(self, plasticity):
        super(Category, self).__init__(plasticity)

    def get_category_of_entity(self, entity):
        # Handle empty entities
        if not entity or not entity.entity:
            return None

        # Person
        elif self.plasticity.sapien.names.is_first_name(entity.entity) and entity.properNoun:
            return "Person"

        # Place
        elif entity.entity in ['hallway', 'bedroom', 'bathroom', 'kitchen', 'office', 'garden']:
            return "Place"

        # Thing
        else:
            return "Thing"