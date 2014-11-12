class HearthStoneDebugLogParser
  def initialize
    @zones = []
  end
  def parse_file(filename)
    File.foreach(filename) {|x| @zones.push(parse_zone_line(x)) if x =~ /^\[Zone\]/  }
    print "parsed file [#{filename}] containing #{@zones.size()} zone lines\n"
#   print @zones.join()
  end
  def parse_zone_line(x)
    x
  end
end

class HearthStoneDebugLogLine
  def initialize(line)
    @object 
  end
end


def words_from_string(string)
  string.downcase.scan(/[\w']+/)
end


#p words_from_string("This is a test of the emergency broadcast system. emergency.com")

parser = HearthStoneDebugLogParser.new();
parser.parse_file("output_log.txt")

