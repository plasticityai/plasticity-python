from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import requests

from plasticity.utils import utils
from plasticity.base.endpoint import Endpoint


class Core(Endpoint):
    """The Core Endpoint performs all the Core API functions described here:
    https://www.plasticity.ai/api/docs/#sapien-core
    """
    def __init__(self, plasticity):
        """Initializes a new Core Endpoint."""
        super(Core, self).__init__(plasticity)
        self._url = self.plasticity.url + "sapien/core/"

    def post(self, text, graph=True, ner=True, pretty=False):
        data = json.dumps({
            'text': text,
            'graph': graph,
            'ner': ner,
            'pretty': pretty
        })
        return self.plasticity._post(self._url, data)

    def get_entity_from_role(self, graph, role):
        return (graph[role] if graph[role] else {}).get('entity', None)

    def sentence_graph(self, text, ner=True, pretty=False):
        """
        Function for the Sentence Graph endpoint

        If ner is enabled, returns an array, where each index is another array
        containing the alternatives for that sentence. If ner is disabled, 
        returns an array, where each index is the graph for that sentence.
        """
        json = self.post(text, graph=True, ner=ner, pretty=pretty)
        response = self.Response(json)
        graphs = []
        if ner:
            for d in response.data:
                alternatives = []
                for a in d.alternatives:
                    alternatives.append(a.graph)
                graphs.append(alternatives)
            return graphs
        else:
            for d in response.data:
                graphs.append(d.graph)
            return graphs

    def coreference_resolution(self, entity, sentence, history):
        """
        Function for the Coreference Resolution endpoint

        history is an array of arrays, where the outer array indices are ordered 
        from oldest to newest entities. The inner array indices all occured in 
        the same sentence.
        """
        tokens = sentence.split(" ")

        # Handle male coreferences
        if entity.entity.lower() in ['he']:
            for outer in reversed(history):
                for inner in outer:
                    if self.plasticity.sapien.names.is_male_name(inner.entity):
                        tokens[entity.index] = inner.entity
                        return " ".join(tokens)

        # Handle female coreferences
        elif entity.entity.lower() in ['she']:
            for outer in reversed(history):
                for inner in outer:
                    if self.plasticity.sapien.names.is_female_name(inner.entity):
                        tokens[entity.index] = inner.entity
                        return " ".join(tokens)

        # Handle plural coreferences
        elif entity.entity.lower() in ['they']:
            resolvedEntities = []
            for outer in reversed(history):
                for inner in outer:
                    if self.plasticity.sapien.names.is_first_name(inner.entity):
                        resolvedEntities.append(inner.entity)
                if len(resolvedEntities) > 1:
                    break
            tokens[entity.index] = " and ".join(resolvedEntities)
            return " ".join(tokens)

        # Caught no coreferences, return the original
        return sentence


    class Response(object):
        """docstring for Response"""
        def __init__(self, res):
            super(Core.Response, self).__init__()

            data = []
            if 'data' in res:
                for d in res['data']:
                    if d['type'] == 'sentenceGroup':
                        data.append(Core.SentenceGroup(d))
                    elif d['type'] == 'sentence':
                        data.append(Core.Sentence(d))

            self.data = data
            self.error = utils.deep_get(res, 'error')

        def __repr__(self):
            return ('<Response %s>' % (id(self)))

        def __str__(self):
            return ('<Response %s>' % (id(self)))


    class SentenceGroup(object):
        """docstring for SentenceGroup"""
        def __init__(self, sg):
            super(Core.SentenceGroup, self).__init__()
            
            alternatives = []
            if 'alternatives' in sg:
                for a in sg['alternatives']:
                    if a['type'] == 'sentence':
                        alternatives.append(Core.Sentence(a))

            self.alternatives = alternatives

        def __repr__(self):
            return ('<SentenceGroup %s>' % (id(self)))

        def __str__(self):
            return ('<SentenceGroup %s>' % (id(self)))
    

    class Sentence(object):
        """docstring for Sentence"""
        def __init__(self, s):
            super(Core.Sentence, self).__init__()

            graph = []
            if 'graph' in s:
                for g in s['graph']:
                    if g['type'] == 'relation':
                        graph.append(Core.Relation(g))

            self.graph = graph
            self.dependencies = utils.deep_get(s, 'dependencies')
            self.sentence = utils.deep_get(s, 'sentence')
            self.tokens = utils.deep_get(s, 'tokens')

        def __repr__(self):
            return ('<Sentence %s>' % (id(self)))

        def __str__(self):
            return ('<Sentence %s>' % (id(self)))
    

    class Relation(object):
        """docstring for Relation"""
        def __init__(self, r):
            super(Core.Relation, self).__init__()

            prepositions = []
            for p in r['prepositions']:
                if p['type'] == 'preposition':
                    prepositions.append(Core.Preposition(p))

            if utils.deep_get(r, 'object', 'type') == 'entity':
                self.object = Core.Entity(r['object'])
            elif utils.deep_get(r, 'object', 'type') == 'relation':
                self.object = Core.Relation(r['object'])
            else:
                self.object = None

            if utils.deep_get(r, 'subject', 'type') == 'entity':
                self.subject = Core.Entity(r['subject'])
            elif utils.deep_get(r, 'subject', 'type') == 'relation':
                self.subject = Core.Relation(r['subject'])
            else:
                self.subject = None

            self.index = utils.deep_get(r, 'index')
            self.predicate = Core.Predicate(r['predicate']) if utils.key_defined_and_has_value(r, 'predicate') else None
            self.prepositions = prepositions
            self.question = utils.deep_get(r, 'question')
            self.questionAuxillary = utils.deep_get(r, 'questionAuxillary')

        def __repr__(self):
            return ('<Relation %s>' % (id(self)))

        def __str__(self):
            return ('<Relation %s>' % (id(self)))


    class Entity(object):
        """docstring for Entity"""
        def __init__(self, e):
            super(Core.Entity, self).__init__()

            self.determiner = utils.deep_get(e, 'determiner')
            self.entity = utils.deep_get(e, 'entity')
            self.entityModifiersPrefix = utils.deep_get(e, 'entityModifiersPrefix')
            self.entityModifiersSuffix = utils.deep_get(e, 'entityModifiersSuffix')
            self.index = utils.deep_get(e, 'index')
            self.ner = utils.deep_get(e, 'ner')
            self.person = utils.deep_get(e, 'person')
            self.possessiveEntity = utils.deep_get(e, 'possessiveEntity')
            self.possessiveSuffix = utils.deep_get(e, 'possessiveSuffix')
            self.properNoun = utils.deep_get(e, 'properNoun')

        def __repr__(self):
            return ('<Entity %s>' % (id(self)))

        def __str__(self):
            return (('%s (Entity)' % (self.entity)) if self.entity else ('(Entity)'))



    class Predicate(object):
        """docstring for Predicate"""
        def __init__(self, p):
            super(Core.Predicate, self).__init__()

            self.auxillaryQualifier = utils.deep_get(p, 'auxillaryQualifier')
            self.conjugation = utils.deep_get(p, 'conjugation')
            self.negated = utils.deep_get(p, 'negated')
            self.phrasalParticle = utils.deep_get(p, 'phrasalParticle')
            self.tense = utils.deep_get(p, 'tense')
            self.verb = utils.deep_get(p, 'verb')
            self.verbModifiersPrefix = utils.deep_get(p, 'verbModifiersPrefix')
            self.verbModifiersSuffix = utils.deep_get(p, 'verbModifiersSuffix')
            self.verbPrefix = utils.deep_get(p, 'verbPrefix')
            self.verbSuffix = utils.deep_get(p, 'verbSuffix')

        def __repr__(self):
            return ('<Predicate %s>' % (id(self)))

        def __str__(self):
            return (('%s (Predicate)' % (self.verb)) if self.verb else ('(Predicate)'))
    

    class Preposition(object):
        """docstring for Preposition"""
        def __init__(self, p):
            super(Core.Preposition, self).__init__()

            if utils.deep_get(p, 'prepositionObject', 'type') == 'entity':
                self.prepositionObject = Core.Entity(p['prepositionObject'])
            elif utils.deep_get(p, 'prepositionObject', 'type') == 'relation':
                self.prepositionObject = Core.Relation(p['prepositionObject'])
            else:
                self.prepositionObject = None

            self.index = utils.deep_get(p, 'index')
            self.preposition = utils.deep_get(p, 'preposition')

        def __repr__(self):
            return ('<Preposition %s>' % (id(self)))

        def __str__(self):
            return (('%s %s (Preposition)' % (self.preposition, self.prepositionObject)) if self.preposition and self.prepositionObject else 
                            ('%s (Preposition)' % (self.preposition)) if self.preposition else ('(Preposition)'))