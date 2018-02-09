from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import requests

from plasticity.utils import utils
from plasticity.base.endpoint import Endpoint


class Core(Endpoint):
    """The Core Endpoint performs all the Core API functions described
    here: https://www.plasticity.ai/api/docs/#sapien-core
    """

    def __init__(self, plasticity):
        """Initializes a new Core Endpoint."""
        super(Core, self).__init__(plasticity)
        self.url = self.plasticity.sapien.url + "core/"

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

    def tpls(self, text, ner=True):
        """Gets each token, its part of speech, and its lemma for each 
        token in the text.

        If ner is enabled, returns an array, where each index is 
        another array containing the [token, POS, lemma]s for each 
        alternative. If ner is disabled, returns an array, where each 
        index is a [token, POS, lemma].
        """
        json = self.post(text, graph=True, ner=ner)
        response = Response.from_json(json)
        output = []
        if ner:
            for sentence_group in response.data:
                alternative_tpls = []
                for sentence in sentence_group.alternatives:
                    alternative_tpls.extend(sentence.tokens)
                output.append(alternative_tpls)
        else:
            for sentence in response.data:
                output.extend(sentence.tokens)
        return output

    def _tpl_helper(self, tpl_index, text, ner=True):
        """Returns either the tokens, pos's, or lemmas for a text.
        Set tpl_index to 0 for tokens, 1 for pos, or 2 for lemmas.

        If ner is enabled, returns an array, where each index is 
        another array containing the t/p/l for each alternative. If 
        ner is disabled, returns an array, where each index is a t/p/l.
        """
        tpls = self.tpls(text, ner=ner)
        output = []
        if ner:
            for alternative in tpls:
                alternative_tpls = [tpl[tpl_index] for tpl in alternative]
                output.append(alternative_tpls)
        else:
            output = [tpl[tpl_index] for tpl in tpls]
        return output

    def tokenize(self, text, ner=True):
        """Handles the Tokenization endpoint.

        If ner is enabled, returns an array, where each index is another 
        array containing the tokens for each alternative. If ner is 
        disabled, returns an array, where each index is a token.
        """
        return self._tpl_helper(0, text, ner)

    def parts_of_speech(self, text, ner=True):
        """Handles the Parts of Speech endpoint.

        If ner is enabled, returns an array, where each index is another 
        array containing the POSs for each alternative. If ner is 
        disabled, returns an array, where each index is a POS.
        """
        return self._tpl_helper(1, text, ner)

    def lemmatize(self, text, ner=True):
        """Handles the Lemmatization endpoint.

        If ner is enabled, returns an array, where each index is another 
        array containing the lemmas for each alternative. If ner is 
        disabled, returns an array, where each index is a lemma.
        """
        return self._tpl_helper(2, text, ner)

    def sentence_graph(self, text, ner=True):
        """Handles the Sentence Graph endpoint. A graph of entities and 
        relationships will appear under the graph key for each sentence. 
        This task provides similar information to the relation 
        extraction task or open information extraction task in NLP.

        If ner is enabled, returns an array, where each index is 
        another array containing the alternatives for that sentence. 
        If ner is disabled, returns an array, where each index is the 
        graph for that sentence.
        """
        json = self.post(text, graph=True, ner=ner)
        response = Response.from_json(json)
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


class Response(object):
    """Holds the `Response` data from a Core API call."""

    def __init__(self, data, error):
        self.data = data
        self.error = error

    def __repr__(self):
        return '<Response %s>' % id(self)

    def __str__(self):
        return '<Response %s>' % id(self)

    @classmethod
    def from_json(cls, res):
        """Builds a `Response` from a json object."""
        data = []
        for d in res.get('data', []):
            if d['type'] == 'sentenceGroup':
                data.append(SentenceGroup.from_json(d))
            elif d['type'] == 'sentence':
                data.append(Sentence.from_json(d))
        error = utils.deep_get(res, 'error')
        return cls(data, error)


class SentenceGroup(object):
    """Holds the `SentenceGroup` data within a `Response` from a 
    Core API call.
    """

    def __init__(self, alternatives):
        self.alternatives = alternatives

    def __repr__(self):
        return '<SentenceGroup %s>' % id(self)

    def __str__(self):
        return '<SentenceGroup %s>' % id(self)

    @classmethod
    def from_json(cls, sg):
        """Builds a `SentenceGroup` from a json object."""
        alternatives = [Sentence.from_json(a)
                        for a in sg.get('alternatives', [])
                        if a.get('type') == 'sentence']
        return cls(alternatives)


class Sentence(object):
    """Holds the `Sentence` data within a `Response` or 
    `SentenceGroup` from a Core API call.
    """

    def __init__(self, sentence, tokens, graph, dependencies):
        self.graph = graph
        self.dependencies = dependencies
        self.sentence = sentence
        self.tokens = tokens

    def __repr__(self):
        return '<Sentence %s>' % id(self)

    def __str__(self):
        return self.sentence

    @classmethod
    def from_json(cls, s):
        """Builds a `Sentence` from a json object."""
        graph = [Relation.from_json(g) for g in s.get('graph', [])
                 if g.get('type') == 'relation']
        dependencies = utils.deep_get(s, 'dependencies')
        sentence = utils.deep_get(s, 'sentence')
        tokens = utils.deep_get(s, 'tokens')
        return cls(sentence, tokens, graph, dependencies)


class Relation(object):
    """Holds the `Relation` data within a `Sentence` from a 
    Core API call.
    """

    def __init__(
            self, subject, predicate, object_, qualifiers, prepositions,
            verb_modifiers_subject_prefix, verb_modifiers_object_prefix,
            question, questionAuxillary):
        self.subject = subject
        self.predicate = predicate
        self.object = object_
        self.qualifiers = qualifiers
        self.prepositions = prepositions
        self.verb_modifiers_subject_prefix = verb_modifiers_subject_prefix
        self.verb_modifiers_object_prefix = verb_modifiers_object_prefix
        self.question = question
        self.questionAuxillary = questionAuxillary

    def __repr__(self):
        return '<Relation %s>' % id(self)

    def __str__(self):
        return '<Relation %s>' % id(self)

    @classmethod
    def from_json(cls, r):
        """Builds a `Relation` from a json object."""
        type_ = utils.deep_get(r, 'subject', 'type')
        subject = (
            Entity.from_json(r['subject']) if type_ == 'entity' else
            Relation.from_json(r['subject']) if type_ == 'relation' else None)
        type_ = utils.deep_get(r, 'object', 'type')
        object_ = (
            Entity.from_json(r['object']) if type_ == 'entity' else
            Relation.from_json(r['object']) if type_ == 'relation' else None)
        prepositions = [Preposition.from_json(p)
                        for p in r.get('prepositions', [])
                        if p.get('type') == 'preposition']
        predicate = Predicate.from_json(utils.deep_get(r, 'predicate'))
        qualifiers = utils.deep_get(r, 'qualifiers')
        vm_subject_prefix = utils.deep_get(r, 'verbModifiersSubjectSuffix')
        vm_object_prefix = utils.deep_get(r, 'verbModifiersObjectSuffix')
        question = utils.deep_get(r, 'question')
        questionAuxillary = utils.deep_get(r, 'questionAuxillary')
        return cls(
            subject, predicate, object_, qualifiers, prepositions,
            vm_subject_prefix, vm_object_prefix, question, questionAuxillary)


class Entity(object):
    """Holds the `Entity` data within a `Relation` from a 
    Core API call. An `Entity` holds information for subjects 
    and objects.
    """

    def __init__(
            self, entity, index, determiner, properNoun, person,
            entity_modifiers_prefix, entity_modifiers_suffix,
            possessive_entity, possessive_suffix, ner):
        self.entity = entity
        self.index = index
        self.determiner = determiner
        self.properNoun = properNoun
        self.person = person
        self.entity_modifiers_prefix = entity_modifiers_prefix
        self.entity_modifiers_suffix = entity_modifiers_suffix
        self.possessive_entity = possessive_entity
        self.possessive_suffix = possessive_suffix
        self.ner = ner

    def __repr__(self):
        return '<Entity %s>' % id(self)

    def __str__(self):
        return self.entity

    @classmethod
    def from_json(cls, e):
        """Builds an `Entity` from a json object."""
        entity = utils.deep_get(e, 'entity')
        index = utils.deep_get(e, 'index')
        determiner = utils.deep_get(e, 'determiner')
        properNoun = utils.deep_get(e, 'properNoun')
        person = utils.deep_get(e, 'person')
        entity_modifiers_prefix = utils.deep_get(e, 'entityModifiersPrefix')
        entity_modifiers_suffix = utils.deep_get(e, 'entityModifiersSuffix')
        possessive_entity = utils.deep_get(e, 'possessive_entity')
        possessive_suffix = utils.deep_get(e, 'possessive_suffix')
        ner = utils.deep_get(e, 'ner')
        return cls(
            entity, index, determiner, properNoun, person,
            entity_modifiers_prefix, entity_modifiers_suffix,
            possessive_entity, possessive_suffix, ner)


class Predicate(object):
    """Holds the `Predicate` data within a `Relation` from a 
    Core API call. A `Predicate` holds information for verbs.
    """

    def __init__(
            self, verb, index, negated, tense, conjugation, phrasal_particle,
            auxillary_qualifier, verb_prefix, verb_suffix, verb_modifiers_prefix,
            verb_modifiers_suffix):
        self.verb = verb
        self.index = index
        self.negated = negated
        self.tense = tense
        self.conjugation = conjugation
        self.phrasal_particle = phrasal_particle
        self.auxillary_qualifier = auxillary_qualifier
        self.verb_prefix = verb_prefix
        self.verb_suffix = verb_suffix
        self.verb_modifiers_prefix = verb_modifiers_prefix
        self.verb_modifiers_suffix = verb_modifiers_suffix

    def __repr__(self):
        return '<Predicate %s>' % id(self)

    def __str__(self):
        return self.verb

    @classmethod
    def from_json(cls, p):
        """Builds a `Predicate` from a json object."""
        verb = utils.deep_get(p, 'verb')
        index = utils.deep_get(p, 'index')
        negated = utils.deep_get(p, 'negated')
        tense = utils.deep_get(p, 'tense')
        conjugation = utils.deep_get(p, 'conjugation')
        phrasal_particle = utils.deep_get(p, 'phrasalParticle')
        auxillary_qualifier = utils.deep_get(p, 'auxillaryQualifier')
        verb_prefix = utils.deep_get(p, 'verbPrefix')
        verb_suffix = utils.deep_get(p, 'verbSuffix')
        verb_modifiers_prefix = utils.deep_get(p, 'verbModifiersPrefix')
        verb_modifiers_suffix = utils.deep_get(p, 'verbModifiersSuffix')
        return cls(
            verb, index, negated, tense, conjugation, phrasal_particle,
            auxillary_qualifier, verb_prefix, verb_suffix,
            verb_modifiers_prefix, verb_modifiers_suffix)


class Preposition(object):
    """Holds the `Preposition` data within a `Relation` from a 
    Core API call.
    """

    def __init__(self, preposition, preposition_object, index):
        self.preposition = preposition
        self.index = index
        self.preposition_object = preposition_object

    def __repr__(self):
        return '<Preposition %s>' % id(self)

    def __str__(self):
        return self.preposition

    @classmethod
    def from_json(cls, p):
        """Builds a `Predicate` from a json object."""
        preposition = utils.deep_get(p, 'preposition')
        index = utils.deep_get(p, 'index')
        type_ = utils.deep_get(p, 'prepositionObject', 'type')
        preposition_object = (
            Entity.from_json(p['prepositionObject']) if type_ == 'entity' else
            Relation.from_json(p['prepositionObject']) if type_ == 'relation'
            else None)
        return cls(preposition, preposition_object, index)
