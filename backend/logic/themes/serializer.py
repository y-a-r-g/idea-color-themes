from types import BooleanType
from backend.logic.themes import elements


def to_str(val):
    if val is None:
        return u'None'
    if type(val) == BooleanType:
        return u'True' if val else u'False'
    return unicode(val)


def from_str(val):
    val = val.strip()
    if val == 'None':
        return None
    if val == 'True':
        return True
    if val == 'False':
        return False
    return val


def serialize_to_lines(theme):
    for (element, params) in theme:
        if isinstance(params, tuple):
            yield '%s=(%s)' % (element, ','.join([to_str(s) for s in params]))
        else:
            yield '%s=%s' % (element, params)


def deserialize_from_lines(lines):
    for line in lines:
        element_params = line.split('=')
        element = element_params[0].strip()
        params = element_params[1].strip()
        if ',' in params:
            params = tuple([from_str(s.strip()) for s in params[1:-1].strip().split(',')])
        else:
            params = from_str(params)
        yield (element, params)


def serialize_to_file(file_or_path, theme):
    if isinstance(file_or_path, str) or isinstance(file_or_path, unicode):
        with open(file_or_path, 'wt') as f:
            f.write('\n'.join(serialize_to_lines(theme)))
    else:
        file_or_path.write('\n'.join(serialize_to_lines(theme)))


def deserialize_from_file(file_or_path):
    if isinstance(file_or_path, str) or isinstance(file_or_path, unicode):
        with open(file_or_path, 'rt') as f:
            return deserialize_from_lines(f.readlines())
    return deserialize_from_lines(file_or_path.readlines())


def serialize_to_idea_lines(theme, name, version=u'1'):
    theme = list(theme)

    yield u'<?xml version="1.0" encoding="UTF-8"?>'
    yield u'<scheme name="%s" version="%s" parent_scheme="Default">' % (name, version)
    yield u'\t<option name="LINE_SPACING" value="1.0" />'
    yield u'\t<option name="EDITOR_FONT_SIZE" value="12" />'
    yield u'\t<option name="EDITOR_FONT_NAME" value="Menlo" />'

    yield u'\t<colors>'
    for (element, parameter) in theme:
        if not isinstance(parameter, tuple):
            yield u'\t\t<option name="%s" value="%s" />' % (element, parameter)
    yield u'\t</colors>'

    yield u'\t<attributes>'
    for (element, parameters) in theme:
        if isinstance(parameters, tuple):
            yield u'\t\t<option name="%s">' % element
            yield u'\t\t\t<value>'
            font = 0
            if parameters[elements.PARAM_BOLD]:
                font += 1
            if parameters[elements.PARAM_ITALIC]:
                font += 2
            if font > 0:
                yield u'\t\t\t\t<option name="FONT_TYPE" value="%d" />' % font
            if not parameters[elements.PARAM_FOREGROUND] is None:
                yield u'\t\t\t\t<option name="FOREGROUND" value="%s" />' % parameters[
                    elements.PARAM_FOREGROUND]
            if not parameters[elements.PARAM_BACKGROUND] is None:
                yield u'\t\t\t\t<option name="BACKGROUND" value="%s" />' % parameters[
                    elements.PARAM_BACKGROUND]
            if not parameters[elements.PARAM_ERROR_STRIPE] is None:
                yield u'\t\t\t\t<option name="ERROR_STRIPE_COLOR" value="%s" />' % \
                      parameters[elements.PARAM_ERROR_STRIPE]
            if not parameters[elements.PARAM_EFFECT_TYPE] is None:
                yield u'\t\t\t\t<option name="EFFECT_TYPE" value="%s" />' % parameters[
                    elements.PARAM_EFFECT_TYPE]
            if not parameters[elements.PARAM_EFFECT_COLOR] is None:
                yield u'\t\t\t\t<option name="EFFECT_COLOR" value="%s" />' % parameters[
                    elements.PARAM_EFFECT_COLOR]
            yield u'\t\t\t</value>'
            yield u'\t\t</option>'
    yield u'\t</attributes>'

    yield u'</scheme>'


def serialize_to_idea_xml(xml, theme, name, version=u'1'):
    if isinstance(xml, str) or isinstance(xml, unicode):
        with open(xml, 'wt') as f:
            f.write('\n'.join(serialize_to_idea_lines(theme, name, version)))
    else:
        xml.write('\n'.join(serialize_to_idea_lines(theme, name, version)))


def get_attribute(line, name, as_color=False):
    if not name in line:
        return None
    attribute = line.split(name)[1].split('"')[1].strip()
    if as_color:
        while len(attribute) < 6:
            attribute = '0' + attribute
    return attribute


def deserialize_from_idea(xml):
    if isinstance(xml, str) or isinstance(xml, unicode):
        with open(xml, 'rt') as f:
            xmlLines = f.readlines()
    elif isinstance(xml, list):
        xmlLines = xml
    else:
        xmlLines = xml.readlines()

    def detect_element(line):
        for element in elements.FLATTEN:
            if element[0] in line.split('"'):
                return element
        return None

    scanLine = 0
    while scanLine < len(xmlLines):
        line = xmlLines[scanLine]
        scanLine += 1

        element = detect_element(line)
        if element:
            if len(element) >= 3 and element[2]:
                yield (element[0], get_attribute(line, 'value', True))
            else:
                params = [None, None, None, None, None, None, None]
                while not '</value>' in line:
                    line = xmlLines[scanLine]
                    scanLine += 1

                    if 'FONT_TYPE' in line:
                        val = get_attribute(line, 'value')
                        if val == '1' or val == '3':
                            params[elements.PARAM_BOLD] = True
                        if val == '2' or val == '3':
                            params[elements.PARAM_ITALIC] = True
                    elif 'FOREGROUND' in line:
                        params[elements.PARAM_FOREGROUND] = get_attribute(line, 'value', True)
                    elif 'BACKGROUND' in line:
                        params[elements.PARAM_BACKGROUND] = get_attribute(line, 'value', True)
                    elif 'ERROR_STRIPE_COLOR' in line:
                        params[elements.PARAM_ERROR_STRIPE] = get_attribute(line, 'value', True)
                    elif 'EFFECT_TYPE' in line:
                        params[elements.PARAM_EFFECT_TYPE] = get_attribute(line, 'value')
                    elif 'EFFECT_COLOR' in line:
                        params[elements.PARAM_EFFECT_COLOR] = get_attribute(line, 'value', True)
                yield (element[0], tuple(params))


def deserialize_from_eclipse_color_theme_xml(xml):
    if isinstance(xml, str) or isinstance(xml, unicode):
        with open(xml, 'rt') as f:
            xmlLines = f.readlines()
    elif isinstance(xml, list):
        xmlLines = xml
    else:
        xmlLines = xml.readlines()

    options = {}

    name = 'Untitled'
    author = 'ideacolorthemes.org'
    website = 'ideacolorthemes.org'

    for line in xmlLines:
        if '<colorTheme' in line:
            name = get_attribute(line, 'name')
            author = get_attribute(line, 'author')
            website = get_attribute(line, 'website')
        elif not '</colorTheme' in line and not '<?xml' in line:
            try:
                option = line.split('<')[1].split(' ')[0].strip()
                color = get_attribute(line, 'color').split('#')[1]
                bold = get_attribute(line, 'bold')
                italic = get_attribute(line, 'italic')

                if get_attribute(line, 'underline'):
                    eff = 1
                elif get_attribute(line, 'strikethrough'):
                    eff = 5
                else:
                    eff = 0

                options[option] = (True if bold else None, True if italic else None, color, None, None,
                                   eff if eff else None, color if eff else None)
            except:
                pass

    bg = 'FFFFFF'
    r = g = b = 255
    if 'background' in options:
        bg = options['background'][elements.PARAM_FOREGROUND]
    if len(bg) == 6:
        r = int(bg[0:2], 16)
        g = int(bg[2:4], 16)
        b = int(bg[4:6], 16)
    elif len(bg) >= 3:
        r = int(bg[0:1], 16)
        g = int(bg[1:2], 16)
        b = int(bg[2:3], 16)
    med = (r + g + b) / (3.0 * 255)
    dark = med < .5

    dependencies = [
        ('TEXT', (None, None, 'foreground', 'background', None, None, None)),
        ('FOLDED_TEXT_ATTRIBUTES',
         (None, None, 'selectionForeground', 'selectionBackground', None, None, None)),
        ('DELETED_TEXT_ATTRIBUTES', (None, None, 'background', 'foreground', None, None, None)),
        ('SEARCH_RESULT_ATTRIBUTES',
         (None, None, None, 'occurrenceIndication', 'occurrenceIndication', None, None)),
        ('WRITE_SEARCH_RESULT_ATTRIBUTES',
         (None, None, None, 'writeOccurrenceIndication', 'writeOccurrenceIndication',
          None, None)),
        ('IDENTIFIER_UNDER_CARET_ATTRIBUTES',
         (None, None, None, 'occurrenceIndication', 'occurrenceIndication', None,
          None)),
        ('WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES', (None, None, None, 'writeOccurrenceIndication',
                                                     'writeOccurrenceIndication', None, None)),
        ('TEXT_SEARCH_RESULT_ATTRIBUTES',
         (None, None, None, 'searchResultIndication', 'searchResultIndication', None,
          None)),
        ('TEMPLATE_VARIABLE_ATTRIBUTES', 'foreground'),
        ('INJECTED_LANGUAGE_FRAGMENT', 'foreground'),
        ('DEPRECATED_ATTRIBUTES', 'deprecatedMember'),
        ('SELECTION_BACKGROUND', 'selectionBackground'),
        ('SELECTION_FOREGROUND', 'selectionForeground'),
        ('CARET_ROW_COLOR', 'currentLine'),
        ('INDENT_GUIDE', 'selectionBackground'),
        ('SELECTED_INDENT_GUIDE', 'selectionForeground'),
        ('LINE_NUMBERS_COLOR', 'lineNumber'),
        ('GUTTER_BACKGROUND', 'background'),
        ('TEARLINE_COLOR', 'currentLine'),
        ('SELECTED_TEARLINE_COLOR', 'selectionBackground'),
        ('METHOD_SEPARATORS_COLOR', 'currentLine'),

        ('BAD_CHARACTER', 'deprecatedMember'),
        ('DEFAULT_KEYWORD', 'keyword'),
        ('DEFAULT_IDENTIFIER', 'foreground'),
        ('DEFAULT_STRING', 'string'),
        ('DEFAULT_VALID_STRING_ESCAPE', 'number'),
        ('DEFAULT_INVALID_STRING_ESCAPE', 'deprecatedMember'),
        ('DEFAULT_NUMBER', 'number'),
        ('DEFAULT_OPERATION_SIGN', 'operator'),
        ('DEFAULT_BRACES', 'bracket'),
        ('DEFAULT_PARENTHS', 'bracket'),
        ('DEFAULT_BRACKETS', 'bracket'),
        ('DEFAULT_DOT', 'operator'),
        ('DEFAULT_COMMA', 'operator'),
        ('DEFAULT_SEMICOLON', 'operator'),
        ('DEFAULT_LINE_COMMENT', 'singleLineComment'),
        ('Block comment', 'multiLineComment'),
        ('DEFAULT_DOC_COMMENT', 'javadoc'),
        ('DEFAULT_DOC_MARKUP', 'javadocKeyword'),
        ('DEFAULT_DOC_COMMENT_TAG', 'javadocTag'),
        ('DEFAULT_LABEL', 'typeParameter'),
        ('DEFAULT_CONSTANT', 'staticFinalField'),
        ('DEFAULT_PREDEFINED_SYMBOL', 'constant'),
        ('DEFAULT_LOCAL_VARIABLE', 'localVariable'),
        ('DEFAULT_GLOBAL_VARIABLE', 'localVariable'),
        ('DEFAULT_FUNCTION_DECLARATION', 'methodDeclaration'),
        ('DEFAULT_FUNCTION_CALL', 'method'),
        ('DEFAULT_PARAMETER', 'typeParameter'),
        ('DEFAULT_INTERFACE_NAME', 'interface'),
        ('DEFAULT_METADATA', 'annotation'),
        ('DEFAULT_CLASS_NAME', 'class'),
        ('DEFAULT_CLASS_REFERENCE', 'class'),
        ('DEFAULT_INSTANCE_METHOD', 'method'),
        ('DEFAULT_INSTANCE_FIELD', 'field'),
        ('DEFAULT_STATIC_METHOD', 'staticMethod'),
        ('DEFAULT_STATIC_FIELD', 'staticField'),
        ('DEFAULT_TAG', 'bracket'),
        ('DEFAULT_ATTRIBUTE', 'typeParameter'),
        ('DEFAULT_ENTITY', 'number'),
        ('DEFAULT_TEMPLATE_LANGUAGE_COLOR', 'foreground'),

        ('CONSOLE_NORMAL_OUTPUT', (None, None, 'foreground', 'background', None, None, None)),
        ('CONSOLE_ERROR_OUTPUT', 'string'),
        ('CONSOLE_USER_INPUT', 'singleLineComment'),
        ('CONSOLE_SYSTEM_OUTPUT', 'number'),
        ('LOG_ERROR_OUTPUT', 'keyword'),
        ('LOG_WARNING_OUTPUT', 'localVariable'),
        ('LOG_EXPIRED_ENTRY', 'multiLineComment'),
        ('CONSOLE_BACKGROUND_KEY', 'background'),

        ('CUSTOM_KEYWORD1_ATTRIBUTES', 'keyword'),
        ('CUSTOM_KEYWORD2_ATTRIBUTES', 'keyword'),
        ('CUSTOM_KEYWORD3_ATTRIBUTES', 'keyword'),
        ('CUSTOM_KEYWORD4_ATTRIBUTES', 'keyword'),
        ('CUSTOM_NUMBER_ATTRIBUTES', 'number'),
        ('CUSTOM_STRING_ATTRIBUTES', 'string'),
        ('CUSTOM_LINE_COMMENT_ATTRIBUTES', 'singleLineComment'),
        ('CUSTOM_MULTI_LINE_COMMENT_ATTRIBUTES', 'multiLineComment'),
        ('CUSTOM_VALID_STRING_ESCAPE_ATTRIBUTES', 'number'),
        ('CUSTOM_INVALID_STRING_ESCAPE_ATTRIBUTES', 'deprecatedMember'),

        #java
        ('DOC_COMMENT_TAG_VALUE', 'javadocKeyword'),
        ('CLASS_NAME_ATTRIBUTES', 'class'),
        ('ANONYMOUS_CLASS_NAME_ATTRIBUTES', 'class'),
        ('TYPE_PARAMETER_NAME_ATTRIBUTES', 'typeParameter'),
        ('ABSTRACT_CLASS_NAME_ATTRIBUTES', 'class'),
        ('INTERFACE_NAME_ATTRIBUTES', 'interface'),
        ('ENUM_NAME_ATTRIBUTES', 'interface'),
        ('IMPLICIT_ANONYMOUS_CLASS_PARAMETER_ATTRIBUTES', 'interface'),
        ('INSTANCE_FIELD_ATTRIBUTES', 'field'),
        ('STATIC_FIELD_ATTRIBUTES', 'staticField'),
        ('PARAMETER_ATTRIBUTES', 'typeParameter'),
        ('ANNOTATION_NAME_ATTRIBUTES', 'javadocKeyword'),
        ('ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES', ''),
        ('STATIC_METHOD_ATTRIBUTES', 'javadocTag'),
        ('METHOD_DECLARATION_ATTRIBUTES', 'method'),
    ]

    def get_option(name):
        if name in options:
            return options[name]
        return None

    def gen_theme():
        for (element, dependency) in dependencies:
            colorElement = False
            for e in elements.FLATTEN:
                if e[0] == element:
                    colorElement = len(e) > 2 and e[2]

            if isinstance(dependency, tuple):
                yield (element, tuple([get_option(t)[elements.PARAM_FOREGROUND]
                                       if t and (not get_option(t) is None) else None
                                       for t in dependency]))
            else:
                opt = get_option(dependency)
                if not opt is None:
                    if colorElement:
                        yield (element, opt[elements.PARAM_FOREGROUND])
                    else:
                        yield (element, opt)

    default_elements = elements.DARK_DEFAULTS if dark else elements.LIGHT_DEFAULTS
    return (name, author, website), list(gen_theme()) + default_elements


def gen_style(params):
    css = ''
    if isinstance(params, tuple):
        if params[elements.PARAM_BOLD]:
            css += 'font-weight: bold; '
        if params[elements.PARAM_ITALIC]:
            css += 'font-style: italic; '
        if not params[elements.PARAM_FOREGROUND] is None:
            css += 'color: #%s;' % params[elements.PARAM_FOREGROUND]
        if not params[elements.PARAM_BACKGROUND] is None:
            css += 'background-color: #%s; ' % params[elements.PARAM_BACKGROUND]
        if params[elements.PARAM_EFFECT_TYPE] == 1:
            css += 'border-bottom: 1px solid #%s; ' % params[elements.PARAM_EFFECT_COLOR]
        if params[elements.PARAM_EFFECT_TYPE] == 5:
            css += 'text-decoration: line-through; text-decoration-color: #%s; ' % params[
                elements.PARAM_EFFECT_COLOR]
    elif params:
        css = 'color #%s; ' % params[0]
    return css


def gen_css(name, theme):
    lines = []
    for (element, params) in theme:
        lines.append('.%s .%s { %s }' % (name, element, gen_style(params)))
    return '\n'.join(lines)