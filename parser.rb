class HearthStoneDebugLogParser
  def initialize
    @zones = []
  end
  def parse_file(filename)
    File.foreach(filename) {|x| @zones.push(parse_zone_line(x.chomp())) if x =~ /^\[Zone\]/  }
#    print "parsed file [#{filename}] containing #{@zones.size()} zone lines\n"
    @zones.select { | x | x.object == "ZoneChangeList" } .each { |x| print parse_event(x) }
    end
  end
  def parse_zone_line(x)
    HearthStoneDebugLogLine.new(x)
  end
  def parse_event(debug_line)
    if debug_line.object == "ZoneChangeList" && debug_line.method == "ProcessChanges" 
      return parse_process_changes(debug_line)
    end
    return nil
  end
  def parse_process_changes(debug_line)
    if debug_line.rest_of_line =~ /TRANSITIONING card/
      if debug_line.rest_of_line =~ /FRIENDLY HAND/
        if debug_line.rest_of_line =~ /name=(.*) id=/
          return HearthStoneEvent.new("TRANSITION",$1,1)
        end
      end
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
  attr_reader :raw_line,:object,:method,:rest_of_line
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


class HearthStoneEvent
  attr_reader :event_type, :card, :sequence_id
  def initialize(event_type,card,sequence_id)
    @event_type = event_type
    @card = card
    @sequence_id = sequence_id
  end
  def to_s
    "#{@event_type} #{@card} #{@sequence_id}\n"
  end

end

class HearthStoneEventTransition < HearthStoneEvent
  attr_reader :destination
end


def words_from_string(string)
  string.downcase.scan(/[\w']+/)
end


#p words_from_string("This is a test of the emergency broadcast system. emergency.com")

parser = HearthStoneDebugLogParser.new();

ARGV.each do |file_name|
  parser.parse_file(file_name)
end
