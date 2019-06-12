from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from plasticity.utils import utils
from plasticity.base.endpoint import Endpoint


class Core(Endpoint):
    """The Core Endpoint performs all the Core API functions described
    here: https://www.plasticity.ai/api/docs/#sapien-core

    Basic usage:

    ```python
    plasticity.sapien.core.post('This is an example.')
    ```


    Arguments:

    text: required
    graph: optional, defaults to True
    ner: optional, defaults to True
    pretty: optional, defaults to False

    ```python
    plasticity.sapien.core.post('This is an example without NER.', ner=False)
    ```


    Returns:

    This returns a custom `Core.Response`, which converts the `data`
    property of a normal `Response` object into either a list of alternative
    `SentenceGroup`s (if NER is enabled) or a list of `Sentence`s. You can
    also use any of the helper methods, documented in the `Core.Response` class
    below.

    ```python
    result = plasticity.sapien.core.post('This is an example.')
    result.tpls()
    ```

    ```python
    result = plasticity.sapien.core.post('Play let it be by The Beatles.')
    for sentence_group in result.data:
        for sentence in sentence_group.alternatives:
            print(sentence.graph)
    ```
    """
    NAME = 'Core'
    PARAMS = [
        ('text',),
        ('graph', True),
        ('ner', True),
        ('pretty', False)
    ]

    def __init__(self, plasticity):
        """Initializes a new Core Endpoint.

        The Core endpoint is used to perform various natural language
        tasks over raw text input.
        :param plasticity: The user's Plasticity holder
        :type plasticity: Plasticity
        """
        super(Core, self).__init__(plasticity)
        self.url = self.plasticity.sapien.url + 'core/'

    class Response(Endpoint.Response):
        def __init__(self, response):
            super(Core.Response, self).__init__(response)
            new_data = []
            for d in (self.data or []):
                if d['type'] == 'sentenceGroup':
                    new_data.append(SentenceGroup.from_json(d))
                elif d['type'] == 'sentence':
                    new_data.append(Sentence.from_json(d))
            self.data = new_data
            self.graph_enabled = self.request.get(
                'graph', Core.get_param_default('graph'))
            self.ner_enabled = self.request.get(
                'ner', Core.get_param_default('ner'))

        def __str__(self):
            """Pretty prints important details about the Core Response."""
            output = 'Core Response'
            if self.error:
                output += ' - {} error:'.format(self.error_code)
                output += '\n'
                output += utils.indent(
                    utils.shorten('{}'.format(self.error_message)))
            else:
                output += ' - {} sentence{}:'.format(
                    len(self.data), '' if len(self.data) == 1 else 's')
                output += '\n'
                for d in self.data:
                    output += utils.indent('{}'.format(d))
                    output += '\n'
            return output

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

        def graphs(self):
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
                raise AttributeError('The `graph` flag must be enabled '
                                     'in your request in order to use '
                                     '`graphs()`.')

            graphs = []
            if self.ner_enabled:
                for sentence_group in self.data:
                    graphs.append(
                        [a.graph for a in sentence_group.alternatives])
            else:
                for sentence in self.data:
                    graphs.append(sentence.graph)
            return graphs

        def dependencies(self):
            """Gets the syntax dependency trees of text.

            The first element in the array is the index of the dependent word.
            The second element in the array is the index of the head word
            (or governor). The third element in the array is the name of the
            dependency relation.

            If ner was enabled, returns a 2D list, where each index is
            another list containing the [index, index, name]s for each
            alternative. If ner was disabled, returns a list, where each
            index is a [index, index, name].
            :returns: The dependencies of the text (index, index, name)
            :rtype: {list}
            """
            output = []
            if self.ner_enabled:
                for sentence_group in self.data:
                    alternative_dependencies = []
                    for sentence in sentence_group.alternatives:
                        alternative_dependencies.extend(sentence.dependencies)
                    output.append(alternative_dependencies)
            else:
                for sentence in self.data:
                    output.extend(sentence.dependencies)
            return output

        def ner(self):
            """Handles the Named Entity Recognition endpoint.

            Provides named entity suggestions for each relation in the text.
            Returns a 3D list, where each index represents a sentence group.
            Each sentence group has a list of alternatives. Each alternative
            has a list of named entities (and their properties).

            That is, the output is structured as:
            >>> results[sentence_index][alternative_index]
            # dict of entities to their token index in the sentence

            :returns: The named entities of the text
            :rtype: {list}
            """
            if not self.ner_enabled or not self.graph_enabled:
                raise AttributeError('The `ner` and `graph` flags must '
                                     'be enabled in your request in order '
                                     'to use `ner()`.')

            data_out = []
            for sentence_group in self.data:
                sentence_group_out = []
                for alternative in sentence_group.alternatives:
                    alternative_out = {}
                    if type(alternative) is Sentence:
                        for graph in alternative.graph:
                            if type(graph) is Relation:
                                entities = graph.get_entities(ner_only=True)
                                alternative_out.update(entities)
                        sentence_group_out.append(alternative_out)
                data_out.append(sentence_group_out)
            return data_out


class SentenceGroup(object):
    """Holds the `SentenceGroup` data within a `CoreResponse` from a
    Core API call.
    """
    def __init__(self, alternatives):
        """Initializes a new `SentenceGroup`.

        A `SentenceGroup` is a list of groupings of `Sentences`, each being
        possible interpretations of the text (if NER is enabled). For example,
        "Find me photos of the beatles" (the insect) vs.
        "Find me photos of The Beatles" (the band).

        :param alternatives: The `Sentence` alternatives
        :type alternatives: {list}
        """
        self.alternatives = alternatives

    def __repr__(self):
        return '<SentenceGroup {}>'.format(id(self))

    def __str__(self):
        output = 'SentenceGroup'
        output += ' - {} alternative{}:'.format(
            len(self.alternatives), '' if len(self.alternatives) == 1 else 's')
        output += '\n'
        for a in self.alternatives:
            output += utils.indent('{}'.format(a))
            output += '\n'
        return output

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
        """Initializes a new `Sentence`.

        Creates a `Sentence` object which holds the data for each sentence in
        the text.
        :param sentence: The sentence text
        :type sentence: string
        :param tokens: A list of the tokens in the sentence
        :type tokens: list
        :param graph: A graph of the relations in the sentence
                      (or none if graph is disabled in the request)
        :type graph: None|list
        :param dependencies: A list of the token dependencies in the sentence
        :type dependencies: list
        """
        self.sentence = sentence
        self.tokens = tokens
        self.graph = graph
        self.dependencies = dependencies

    def __repr__(self):
        return '<Sentence {}>'.format(id(self))

    def __str__(self):
        output = 'Sentence:'
        output += '\n'
        output += utils.indent(
            utils.fill('Text: {}'.format(self.sentence)))
        output += '\n\n'
        output += utils.indent(
            utils.shorten('Tokens: {}'.format(str(self.tokens))))
        output += '\n\n'
        output += utils.indent(
            utils.shorten('Dependencies: {}'.format(str(self.dependencies))))
        if self.graph is not None:
            output += '\n\n'
            output += utils.indent('Graph: {} relation{}'.format(
                len(self.graph), '' if len(self.graph) == 1 else 's'))
        return output

    @classmethod
    def from_json(cls, s):
        """Builds a `Sentence` from a json object."""
        sentence = s.get('sentence')
        tokens = s.get('tokens')
        graph = s.get('graph')
        if graph is not None:
            graph = Graph.from_json(graph)
        dependencies = s.get('dependencies')
        return cls(sentence, tokens, graph, dependencies)


class Graph(list):
    """Holds the `Graph` data within a `Sentence` from a
    Core API call.

    Returns a `Graph`, which will be an empty list or a list with each
    `Relation` contained in the `Sentence`.
    """
    def __init__(self, *args, **kwargs):
        super(Graph, self).__init__(args[0])

    def __repr__(self):
        return '<Graph {}>'.format(id(self))

    def __str__(self):
        output = 'Graph'
        output += ' - {} relation{}:'.format(
            len(self), '' if len(self) == 1 else 's')
        output += '\n'
        for x in self:
            output += utils.indent('{}'.format(x))
            output += '\n'
        return output

    @classmethod
    def from_json(cls, g):
        """Builds a `Graph` from a json object."""
        graph = [Relation.from_json(x) for x in g
                 if x.get('type') == 'relation']
        return cls(graph)


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
        return '<Relation {}>'.format(id(self))

    def __str__(self):
        output = 'Relation:'
        output += '\n'
        output += utils.indent('Subject: {}'.format(repr(self.subject)))
        output += '\n'
        output += utils.indent('Predicate: {}'.format(repr(self.predicate)))
        output += '\n'
        output += utils.indent('Object: {}'.format(repr(self.object)))
        output += '\n'
        output += utils.indent(utils.shorten(
            'Prepositions: {}'.format(str(self.prepositions))))
        output += '\n'
        return output

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
        predicate = Predicate.from_json(r.get('predicate'))
        qualifiers = r.get('qualifiers')
        vm_subject_prefix = r.get('verbModifiersSubjectSuffix')
        vm_object_prefix = r.get('verbModifiersObjectSuffix')
        question = r.get('question')
        question_auxiliary = r.get('questionAuxiliary')
        return cls(
            subject, predicate, object_, qualifiers, prepositions,
            vm_subject_prefix, vm_object_prefix, question, question_auxiliary)

    def get_entities(self, ner_only=False):
        """Gets the entities of a `Relation`.

        Gets the named entities from a relation by cycling through
        the subjects and objects deeply.
        :param ner_only: Only entities with NER values, defaults to False
        :type ner_only: bool, optional
        :returns: A dict of entities found in the Relation by their index
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
                if not ner_only or (ner_only and x.ner):
                    if x.index not in entities:
                        values = {}
                        values['index'] = x.index
                        values['entity'] = x.entity
                        if x.ner:
                            values['ner'] = x.ner
                        entities[x.index] = values
            elif type(x) is Relation:
                get_entities_helper(x.subject, entities)
                get_entities_helper(x.object, entities)
                for preposition in x.prepositions:
                    get_entities_helper(preposition.preposition_object)
            return entities
        entities = get_entities_helper(self)
        return entities


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
        return '<Entity {}>'.format(id(self))

    def __str__(self):
        output = 'Entity:'
        output += '\n'
        output += utils.indent('Index: {}'.format(self.index))
        output += '\n'
        output += utils.indent('Determiner: {}'.format(self.determiner))
        output += '\n'
        output += utils.indent('Entity: {}'.format(self.entity))
        output += '\n'
        output += utils.indent(utils.shorten(
            'Modifiers Prefix: {}'.format(str(self.entity_modifiers_prefix))))
        output += '\n'
        output += utils.indent(utils.shorten(
            'Modifiers Suffix: {}'.format(str(self.entity_modifiers_suffix))))
        output += '\n'
        return output

    @classmethod
    def from_json(cls, e):
        """Builds an `Entity` from a json object."""
        entity = e.get('entity')
        index = e.get('index')
        determiner = e.get('determiner')
        proper_noun = e.get('properNoun')
        person = e.get('person')
        entity_modifiers_prefix = e.get('entityModifiersPrefix')
        entity_modifiers_suffix = e.get('entityModifiersSuffix')
        possessive_entity = e.get('possessive_entity')
        possessive_suffix = e.get('possessive_suffix')
        ner = e.get('ner')
        if ner is not None:
            ner = [Concept.from_json(c) for c in ner
                   if c.get('type') == 'concept']
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
            auxiliary_qualifier, verb_prefix, verb_suffix,
            verb_modifiers_prefix, verb_modifiers_suffix):
        self.verb = verb
        self.index = index
        self.negated = negated
        self.tense = tense
        self.conjugation = conjugation
        self.phrasal_particle = phrasal_particle
        self.auxiliary_qualifier = auxiliary_qualifier
        self.verb_prefix = verb_prefix
        self.verb_suffix = verb_suffix
        self.verb_modifiers_prefix = verb_modifiers_prefix
        self.verb_modifiers_suffix = verb_modifiers_suffix

    def __repr__(self):
        return '<Predicate {}>'.format(id(self))

    def __str__(self):
        output = 'Predicate:'
        output += '\n'
        output += utils.indent('Index: {}'.format(self.index))
        output += '\n'
        output += utils.indent('Verb: {}'.format(self.determiner))
        output += '\n'
        output += utils.indent('Prefix: {}'.format(self.verb_prefix))
        output += '\n'
        output += utils.indent('Suffix: {}'.format(self.verb_suffix))
        output += '\n'
        output += utils.indent(utils.shorten(
            'Modifiers Prefix: {}'.format(str(self.verb_modifiers_prefix))))
        output += '\n'
        output += utils.indent(utils.shorten(
            'Modifiers Suffix: {}'.format(str(self.verb_modifiers_suffix))))
        output += '\n'
        return output

    @classmethod
    def from_json(cls, p):
        """Builds a `Predicate` from a json object."""
        verb = p.get('verb')
        index = p.get('index')
        negated = p.get('negated')
        tense = p.get('tense')
        conjugation = p.get('conjugation')
        phrasal_particle = p.get('phrasalParticle')
        auxiliary_qualifier = p.get('auxiliaryQualifier')
        verb_prefix = p.get('verbPrefix')
        verb_suffix = p.get('verbSuffix')
        verb_modifiers_prefix = p.get('verbModifiersPrefix')
        verb_modifiers_suffix = p.get('verbModifiersSuffix')
        return cls(
            verb, index, negated, tense, conjugation, phrasal_particle,
            auxiliary_qualifier, verb_prefix, verb_suffix,
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
        return '<Preposition {}>'.format(id(self))

    def __str__(self):
        output = 'Preposition:'
        output += '\n'
        output += utils.indent('Index: {}'.format(self.index))
        output += '\n'
        output += utils.indent('Preposition: {}'.format(self.preposition))
        output += '\n'
        output += utils.indent('Object: {}'.format(self.preposition_object))
        output += '\n'
        return output

    @classmethod
    def from_json(cls, p):
        """Builds a `Predicate` from a json object."""
        preposition = p.get('preposition')
        index = p.get('index')
        type_ = utils.deep_get(p, 'prepositionObject', 'type')
        preposition_object = (
            Entity.from_json(p['prepositionObject']) if type_ == 'entity' else
            Relation.from_json(p['prepositionObject']) if type_ == 'relation'
            else None)
        return cls(preposition, preposition_object, index)


class Concept(object):
    """Holds the `Concept` data within an `Entity` from a
    Core API call.
    """
    def __init__(self, label, id_, freebase_id):
        self.label = label
        self.id_ = id_
        self.freebase_id = freebase_id

    def __repr__(self):
        return '<Concept {}>'.format(id(self))

    def __str__(self):
        output = 'Concept:'
        output += '\n'
        output += utils.indent('Label: {}'.format(self.label))
        output += '\n'
        output += utils.indent('ID: {}'.format(self.id_))
        output += '\n'
        output += utils.indent('Freebase ID: {}'.format(self.freebase_id))
        output += '\n'
        return output

    @classmethod
    def from_json(cls, c):
        """Builds a `Concept` from a json object."""
        label = c.get('label')
        id_ = c.get('id')
        freebase_id = c.get('freebaseIdentifier')
        return cls(label, id_, freebase_id)
