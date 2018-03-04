class Util:
    def is_out_of_areas(num, areas):
        for area in areas:
            if area[0] < num and num < area[1]:
                return False
        return True


    def format(items):
        headings = []
        for item in items:
            headings.append(item[0])
        # --------------------------

        # minimize diff between headings -----
        _depths = list(set(headings))  # sort and unique
        # replace with depth rank
        for i, item in enumerate(headings):
            headings[i] = _depths.index(headings[i]) + 1
        # ----- /minimize diff between headings

        # --------------------------
        for i, item in enumerate(items):
            item[0] = headings[i]
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
