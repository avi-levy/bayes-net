def enum(evidence, trace, ret) :
        ev = ""
        for key in sorted(evidence.keys()):
                ev += "%s=%s " % (key, evidence[key])
        print "%s| %s = %1.8f" % (trace.ljust(14), ev.ljust(30), ret)
