import re
from clldutils.path import Path
import sails


class Icons(object):
    filename_pattern = re.compile('(?P<spec>(c|d|s|f|t)[0-9a-f]{3})\.png')
    graytriangle = "tcccccc"

    @staticmethod
    def id(spec):
        """translate old wals icon id into clld icon id c0a9 -> c00aa99
        """
        return ''.join(c if i == 0 else c + c for i, c in enumerate(spec))

    def __init__(self):
        self._icons = []
        for name in sorted(
                [fn.name for fn in
                Path(sails.__file__).parent.joinpath('static', 'icons').glob('*.png')]):
            m = self.filename_pattern.match(name)
            if m:
                self._icons.append(Icons.id(m.group('spec')))

    def __iter__(self):
        return iter(self._icons)

    def iconize(self, xs, t = "c"):
        icons_t = sorted([icon for icon in self._icons if icon.startswith(t)])
        icons_selection = [icons_t[i] for i in xrange(0, len(icons_t), len(icons_t)/len(xs))]
        return dict(zip(xs, icons_selection))

    def iconizeall(self, xs):
        icons_t = sorted([icon for icon in self._icons])
        icons_selection = [icons_t[i] for i in xrange(0, len(icons_t), len(icons_t)/len(xs))]
        return dict(zip(xs, icons_selection))
