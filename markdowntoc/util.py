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
