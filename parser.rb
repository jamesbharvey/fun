class HearthStoneDebugLogParser
  def initialize
    @zones = []
  end
  def parse_file(filename)
    File.foreach(filename) {|x| @zones.push(parse_zone_line(x.chomp())) if x =~ /^\[Zone\]/  }
#    print "parsed file [#{filename}] containing #{@zones.size()} zone lines\n"
    print @zones.join("\n")
  end
  def parse_zone_line(x)
    HearthStoneDebugLogLine.new(x)
  end
end


# ZoneChangeList.Finish
# ZoneChangeList.FireCompleteCallback
# ZoneChangeList.OnUpdateLayoutComplete
# ZoneChangeList.ProcessChanges
# ZoneChangeList.UpdateDirtyZones
# ZoneMgr.AddServerZoneChanges
# ZoneMgr.CreateLocalChangeList
# ZoneMgr.CreateLocalChangesFromTrigger
# ZoneMgr.ProcessLocalChangeList


class HearthStoneDebugLogLine
  attr_reader :raw_line,:object,:method
  def initialize(line)
    @raw_line = line
    line =~ /^\[Zone\] (Zone\w+)\.(\w+)\W+(.*)/ 
    @object = $1
    @method = $2
    @rest_of_line = $3;
  end
  def to_s
    "#{@object}.#{@method} #{@rest_of_line} [[[[[#{@raw_line}]]]]]"
  end
end


def words_from_string(string)
  string.downcase.scan(/[\w']+/)
end


#p words_from_string("This is a test of the emergency broadcast system. emergency.com")

parser = HearthStoneDebugLogParser.new();

ARGV.each do |file_name|
  parser.parse_file(file_name)
end
