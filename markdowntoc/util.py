import collections

class Util:
    def is_out_of_areas(num, areas):
        for area in areas:
            if area[0] < num and num < area[1]:
                return False
        return True


    def format(items):
        levels = []
        for item in items:
            levels.append(item[0])
        # --------------------------

        # minimize diff between levels -----
        _depths = list(set(levels))  # sort and unique
        # replace with depth rank
        for i, item in enumerate(levels):
            levels[i] = _depths.index(levels[i]) + 1


        # Force set level of first item to 1 -----
        # (first item must be list root)
        if len(levels):
            diff_to_root = levels[0] - 1
            if 0 < diff_to_root:
                def pad(level):
                    return level - diff_to_root
                levels = list(map(pad, levels))

        # --------------------------
        for i, item in enumerate(items):
            item[0] = levels[i]
        return items


    def strtobool(val):
        """pick out from 'distutils.util' module"""
        if isinstance(val, str):
            val = val.lower()
            if val in ('y', 'yes', 't', 'true', 'on', '1'):
                return 1
            elif val in ('n', 'no', 'f', 'false', 'off', '0'):
                return 0
            else:
                raise ValueError("invalid truth value %r" % (val,))
        else:
            return bool(val)


    def within_ranges(target, ranges):
        tb = target[0]
        te = target[1]
        for _range in ranges:
            rb = _range[0]
            re = _range[1]
            if (rb <= tb and tb <= re) and (rb <= tb and tb <= re):
                return True
        return False

    # This method is from https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
    def dict_merge(dct, merge_dct):
        """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
        updating only top-level keys, dict_merge recurses down into dicts nested
        to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
        ``dct``.
        :param dct: dict onto which the merge is executed
        :param merge_dct: dct merged into dct
        :return: None
        """
        for k, v in merge_dct.items():
            if (k in dct and isinstance(dct[k], dict)
                    and isinstance(merge_dct[k], collections.Mapping)):
                Util.dict_merge(dct[k], merge_dct[k])
            else:
                dct[k] = merge_dct[k]