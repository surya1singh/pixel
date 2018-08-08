from optparse import OptionParser

USAGE = "Arguments for Subimage"

class OptParser:
    @classmethod
    def parseopts(self):
        try:
            parser = OptionParser(usage = USAGE)

            parser.add_option("-d", "--directory", action = "store",
                                                 type = "string",
                                                 help = "path for images directory",
                                                 dest = "directory",
                             )

            parser.add_option("-c", "--child", action = "store",
                                                 type = "string",
                                                 help = "child image full path with name",
                                                 dest = "child",
                             )
            parser.add_option("-p", "--parent", action = "store",
                                                 type = "string",
                                                 help = "parent image full path with name",
                                                 dest = "parent",
                             )
            try:
                (options, args) = parser.parse_args()
            except:
                raise OptionParserError

            if options.directory or (options.child and options.parent):
                kwargs = {
                    "directory": options.directory,
                    "child": options.child,
                    "parent": options.parent,
                }
                return kwargs
            raise ValueError('There is some invalid inputs \n')
        except ValueError:
            raise ValueError('Type -h for help \n\t %s' % USAGE)
