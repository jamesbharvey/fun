class HearthStoneDebugLogParser
  def usage
    puts "Please pass the file(s)to be parsed as command line arguments."
  end
  def initialize
    @zones = []
  end
  def parse_file(filename)
    File.foreach(filename) {|x| @zones.push(parse_zone_line(x.chomp())) if x =~ /^\[Zone\]/  }
#    print "parsed file [#{filename}] containing #{@zones.size()} zone lines\n"
    @zones.select { | x | x.object == "ZoneChangeList" } .collect { |x| parse_event(x) }. select { |x| x != nil }.each {|x| print "#{x.pretty_s}\n" }
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
        if debug_line.rest_of_line =~ /name=(.*) id=(\d+)/
          print debug_line.rest_of_line,"\n"
          return HearthStoneEventCardDraw.new($1,$2,"FRIENDLY HAND")
        end
      end
      if debug_line.rest_of_line =~ /OPPOSING HAND/ 
        if debug_line.rest_of_line =~ /id=(\d+)/
          print debug_line.rest_of_line,"\n"
          return HearthStoneEventCardDraw.new("a card",$1,"OPPOSING HAND")
        end
      end
      if debug_line.rest_of_line =~ /FRIENDLY PLAY/ 
        return nil if debug_line.rest_of_line =~ /\(Hero\)$/
        if debug_line.rest_of_line =~ /name=(.*) id=(\d+)/
          print debug_line.rest_of_line,"\n"
          return HearthStoneEventCardPlay.new($1,$2,"FRIENDLY PLAY")
        end
      end
      if debug_line.rest_of_line =~ /OPPOSING PLAY/ 
        return nil if debug_line.rest_of_line =~ /\(Hero\)$/
        if debug_line.rest_of_line =~ /name=(.*) id=(\d+)/
          print debug_line.rest_of_line,"\n"
          return HearthStoneEventCardPlay.new($1,$2,"OPPOSING PLAY")
        end
      end
      return nil
    end

    return nil
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
    "#{@event_type} #{@card} #{@sequence_id}"
  end
  def pretty_s
    to_s
  end

end

class HearthStoneEventCardTransition < HearthStoneEvent
  attr_reader :destination
  def initialize(card,sequence_id,destination)
    super("TRANSITION",card,sequence_id)
    @destination = destination
  end
  def to_s
    "#{super} #{@destination}\n"
  end
end

class HearthStoneEventCardDraw < HearthStoneEventCardTransition
  def pretty_s
    "#{@destination} drew #{@card} id=#{sequence_id}"
  end
end

class HearthStoneEventCardPlay < HearthStoneEventCardTransition
  def pretty_s
    "#{@destination} #{@card} id=#{sequence_id}"
  end
end

ARGV

parser = HearthStoneDebugLogParser.new();

parser.usage unless ARGV.size > 0;

ARGV.each do |file_name|
  parser.parse_file(file_name)
end
