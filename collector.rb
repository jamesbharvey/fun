

require 'fileutils'

##
## where to look for the debug log that hearthstone outputs
##
log_file = "D:\\Program Files (x86)\\Hearthstone\\Hearthstone_Data\\output_log.txt"

##
## where to keep the files that we are going to archive
## 
## CREATE THIS DIRECTORY BEFORE YOU RUN THIS PROGRAM
##

archive_directory = "C:\\Users\\James\\projects\\HearthStoneDebugLog\\archive"

##
## get the newest file in the archive for us to compare against the most 
## recent live log
##

Dir.chdir(archive_directory)
newest = Dir.entries(archive_directory).sort_by { |x| File.ctime(x) }.reverse[0]

##
## exit if the newest file in the archive is newer than the
## current log file
##

exit if File.mtime(newest) >= File.mtime(log_file);

##
## if we get here, there is a new file. Don't copy it if it looks like
## hearthstone is open right now. Check this by seeing if the file has
## a handle open on it, using the sysinternal handle utility
##

rv = `C:\\Users\\James\\sysinternals\\handle.exe output_log`
rv = rv.gsub(/\n/,'')
if not (/No matching handles found/.match(rv))
  exit
end

##
## copy the file finally
##

new_filename = File.mtime(log_file).strftime("%Y%m%d%H%M%Soutput_log.txt")
FileUtils.copy log_file,  new_filename
