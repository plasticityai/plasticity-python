from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

from plasticity.utils import utils
from plasticity.base.endpoint import Endpoint
from plasticity.base.response import Response


class Core(Endpoint):
    """The Core Endpoint performs all the Core API functions described
    here: https://www.plasticity.ai/api/docs/#sapien-core
    """
    def __init__(self, plasticity):
        """Initializes a new Core Endpoint.

        The Core endpoint is used to perform various natural language
        tasks over raw text input.
        :param plasticity: The user's Plasticity holder
        :type plasticity: Plasticity
        """
        super(Core, self).__init__(plasticity)
        self.url = self.plasticity.sapien.url + "core/"

    def post(self, text, graph=True, ner=True, pretty=False):
        """Makes a post to the Core API.

        Runs the text with the requested parameters through the Sapien
        Core API.
        :param text: The sentence or sentences to analyze
        :type text: str
        :param graph: Whether or not to enable the graph, defaults to True
        :type graph: bool, optional
        :param ner: Whether or not to enable NER, defaults to True
        :type ner: bool, optional
        :param pretty: Whether or not to pretty print, defaults to False
        :type pretty: bool, optional
        :returns: The response from the API endpoint
        :rtype: {CoreResponse}
        """
        payload = json.dumps({
            'text': text,
            'graph': graph,
            'ner': ner,
            'pretty': pretty,
        })
        res = self.plasticity._post(self.url, payload)
        return CoreResponse.from_json(
            res, graph_enabled=graph, ner_enabled=ner, pretty_enabled=pretty)

    def get_entity_from_role(self, graph, role):
        """Gets the entity from a role.

        :param graph: The sentence graph
        :type graph: dict
        :param role: The role to get the entity from
        :type role: str
        """
        return (graph[role] or {}).get('entity', None)


class CoreResponse(Response):
    """Holds the `CoreResponse` data from a Core API call."""
    def __init__(self, *args, **kwargs):
        super(CoreResponse, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<CoreResponse %s>' % id(self)

    def __str__(self):
        return '<CoreResponse %s>' % id(self)

    @classmethod
    def from_json(
            cls, res, graph_enabled=True, ner_enabled=True,
            pretty_enabled=False):
        """Builds a `CoreResponse` from a json object."""
        data = []
        for d in res.get('data', []):
            if d['type'] == 'sentenceGroup':
                data.append(SentenceGroup.from_json(d))
            elif d['type'] == 'sentence':
                data.append(Sentence.from_json(d))
        error = utils.deep_get(res, 'error')
        return cls(
            data, error, graph_enabled=graph_enabled, ner_enabled=ner_enabled,
            pretty_enabled=pretty_enabled)

    def tpls(self):
        """Gets the token/POS/lemma of text.

        Gets each token, its part of speech, and its lemma for each
        token in the text.

        If ner was enabled, returns a 2D list, where each index is
        another list containing the [token, POS, lemma]s for each
        alternative. If ner was disabled, returns a list, where each
        index is a [token, POS, lemma].
        :returns: The t/p/l's of the text (token, POS, lemma)
        :rtype: {list}
        """
        output = []
        if self.ner_enabled:
            for sentence_group in self.data:
                alternative_tpls = []
                for sentence in sentence_group.alternatives:
                    alternative_tpls.extend(sentence.tokens)
                output.append(alternative_tpls)
        else:
            for sentence in self.data:
                output.extend(sentence.tokens)
        return output

    def _tpl_helper(self, tpl_index):
        """A helper for the `tpls()` function.

        Returns either the tokens, pos's, or lemmas for a text.
        Set tpl_index to 0 for tokens, 1 for pos, or 2 for lemmas.

        If ner was enabled, returns a 2D list, where each index is
        another list containing the t/p/l for each alternative. If
        ner was disabled, returns a list, where each index is a t/p/l.
        """
        tpls = self.tpls()
        output = []
        if self.ner_enabled:
            for alternative in tpls:
                output.append([tpl[tpl_index] for tpl in alternative])
        else:
            output = [tpl[tpl_index] for tpl in tpls]
        return output

    def tokenize(self):
        """Handles the Tokenization endpoint.

        Tokenizes each word in the text.

        If ner was enabled, returns a 2D list, where each index is another
        list containing the tokens for each alternative. If ner was
        disabled, returns a list, where each index is a token.
        :returns: The tokens of the text
        :rtype: {list}
        """
        return self._tpl_helper(0)

    def parts_of_speech(self):
        """Handles the Parts of Speech endpoint.

        Gets the parts of speech of each token in the text.

        If ner was enabled, returns a 2D list, where each index is another
        list containing the POSs for each alternative. If ner was
        disabled, returns a list, where each index is a POS.
        :returns: The parts of speech of the text
        :rtype: {list}
        """
        return self._tpl_helper(1)

    def lemmatize(self):
        """Handles the Lemmatization endpoint.

        Gets the lemmas of each token in the text.

        If ner was enabled, returns a 2D list, where each index is another
        list containing the lemmas for each alternative. If ner was
        disabled, returns a list, where each index is a lemma.
        :returns: The parts of speech of the text
        :rtype: {list}
        """
        return self._tpl_helper(2)

    def sentence_graph(self):
        """Handles the Sentence Graph endpoint.

        A graph of entities and relationships will appear under the
        graph key for each sentence. This task provides similar information
        to the relation extraction task or open information extraction task
        in NLP.

        If ner was enabled, returns a 3D list, where each index represents
        a sentence group. Each sentence group has a list of alternatives.
        Each alternative has a graph of relation(s). If ner was disabled,
        returns a list, where each index is the graph for that sentence.
        :returns: The graphs of the text
        :rtype: {list}
        """
        if not self.graph_enabled:
            raise AttributeError('The `graph` flag must be enabled in your '
                                 'request in order to use `sentence_graph()`.')

        graphs = []
        if self.ner_enabled:
            for d in self.data:
                graphs.append([a.graph for a in d.alternatives])
            return graphs
        else:
            for d in self.data:
                graphs.append(d.graph)
            return graphs

    def ner(self):
        """Handles the Named Entity Recognition endpoint.

        Provides named entity suggestions for each relation in the text.
        Returns a 3D list, where each index represents a sentence group.
        Each sentence group has a list of alternatives. Each alternative
        has a list of named entities (and their properties).
        :returns: The named entities of the text
        :rtype: {list}
        """
        if not self.ner_enabled:
            raise AttributeError('The `ner` flag must be enabled in your '
                                 'request in order to use `ner()`.')

        sentence_graph = self.sentence_graph()
        data_out = []
        for sentence_group in sentence_graph:
            sentence_group_out = []
            for alternative in sentence_group:
                alternative_out = []
                for relation in alternative:
                    entities = [e for e in relation.get_entities() if e['ner']]
                    alternative_out.append(entities)
                sentence_group_out.append(alternative_out)
            data_out.append(sentence_group_out)
        return data_out

    def ner_replace(self):
        """Helper for the Named Entity Recognition endpoint.

        Replaces entities with their corrected form. For example, the sentence
        "pixar produced toy story" is corrected to "Pixar produced Toy Story".
        Since NER is enabled for this request, entity-corrected text will be
        returned for each alternative. Therefore, there may be sentence
        duplicates in the returned list. There also may be different
        variations in the returned list.
        :returns: The entity-correct text alternatives
        :rtype: {list}
        """
        if not self.ner_enabled:
            raise AttributeError('The `ner` flag must be enabled in your '
                                 'request in order to use `ner_replace()`.')

        ner = self.ner()
        data_out = []
        for sg_data, sg_ner in zip(self.data, ner):
            sentence_group_out = []
            for alt_data, alt_ner in zip(sg_data.alternatives, sg_ner):
                # Replace the text in the sentence with the named entities
                new_sentence = alt_data.sentence
                for graph in alt_ner:
                    for entity in graph:
                        new_sentence = new_sentence.replace(
                            entity['entity'], entity['ner'][0]['label'])
                sentence_group_out.append(new_sentence)
            data_out.append(sentence_group_out)
        return data_out


class SentenceGroup(object):
    """Holds the `SentenceGroup` data within a `CoreResponse` from a
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
    """Holds the `Sentence` data within a `CoreResponse` or
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
            question, question_auxiliary):
        self.subject = subject
        self.predicate = predicate
        self.object = object_
        self.qualifiers = qualifiers
        self.prepositions = prepositions
        self.verb_modifiers_subject_prefix = verb_modifiers_subject_prefix
        self.verb_modifiers_object_prefix = verb_modifiers_object_prefix
        self.question = question
        self.question_auxiliary = question_auxiliary

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
        question_auxiliary = utils.deep_get(r, 'questionAuxiliary')
        return cls(
            subject, predicate, object_, qualifiers, prepositions,
            vm_subject_prefix, vm_object_prefix, question, question_auxiliary)

    def get_entities(self, ner=True):
        """Gets the entities of a `Relation`.

        Gets the named entities from a relation by cycling through
        the subjects and objects deeply.
        :param ner: Whether or not to return the NER values, defaults to True
        :type ner: bool, optional
        :returns: The index of each entity to the entities themselves
        :rtype: {dict}
        """
        def get_entities_helper(x, entities={}):
            """Gets the entities in a subject or object.

            :param x: Relation's subject or object
            :type x: Entity or Relation
            :param entities: The cumulative entities found, defaults to {}
            :type entities: dict, optional
            """
            if type(x) is Entity:
                if x.index not in entities:
                    values = {}
                    values['index'] = x.index
                    values['entity'] = x.entity
                    if ner:
                        values['ner'] = x.ner
                    entities[x.index] = values
            elif type(x) is Relation:
                get_entities_helper(x.subject, entities)
                get_entities_helper(x.object, entities)
            return entities.values()
        return get_entities_helper(self)


class Entity(object):
    """Holds the `Entity` data within a `Relation` from a
    Core API call. An `Entity` holds information for subjects
    and objects.
    """
    def __init__(
            self, entity, index, determiner, proper_noun, person,
            entity_modifiers_prefix, entity_modifiers_suffix,
            possessive_entity, possessive_suffix, ner):
        self.entity = entity
        self.index = index
        self.determiner = determiner
        self.proper_noun = proper_noun
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
        proper_noun = utils.deep_get(e, 'properNoun')
        person = utils.deep_get(e, 'person')
        entity_modifiers_prefix = utils.deep_get(e, 'entityModifiersPrefix')
        entity_modifiers_suffix = utils.deep_get(e, 'entityModifiersSuffix')
        possessive_entity = utils.deep_get(e, 'possessive_entity')
        possessive_suffix = utils.deep_get(e, 'possessive_suffix')
        ner = utils.deep_get(e, 'ner')
        return cls(
            entity, index, determiner, proper_noun, person,
            entity_modifiers_prefix, entity_modifiers_suffix,
            possessive_entity, possessive_suffix, ner)


class Predicate(object):
    """Holds the `Predicate` data within a `Relation` from a
    Core API call. A `Predicate` holds information for verbs.
    """
    def __init__(
            self, verb, index, negated, tense, conjugation, phrasal_particle,
            auxillary_qualifier, verb_prefix, verb_suffix,
            verb_modifiers_prefix, verb_modifiers_suffix):
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
