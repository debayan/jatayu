#!/usr/bin/env ruby
require 'google/apis/calendar_v3'
require 'googleauth'
require 'googleauth/stores/file_token_store'

require 'fileutils'
require 'optparse'
require 'chronic'

OOB_URI = 'urn:ietf:wg:oauth:2.0:oob'
APPLICATION_NAME = 'Jatayu'
CLIENT_SECRETS_PATH = File.join(Dir.pwd, 'executables', 'client_secret.json')
CREDENTIALS_PATH = File.join(Dir.home, '.credentials',
                             "calendar-ruby-quickstart.yaml")
SCOPE = Google::Apis::CalendarV3::AUTH_CALENDAR

MAX_EVENTS = 3

##
# Ensure valid credentials, either by restoring from the saved credentials
# files or intitiating an OAuth2 authorization. If authorization is required,
# the user's default browser will be launched to approve the request.
#
# @return [Google::Auth::UserRefreshCredentials] OAuth2 credentials
def authorize
  FileUtils.mkdir_p(File.dirname(CREDENTIALS_PATH))

  client_id = Google::Auth::ClientId.from_file(CLIENT_SECRETS_PATH)
  token_store = Google::Auth::Stores::FileTokenStore.new(file: CREDENTIALS_PATH)
  authorizer = Google::Auth::UserAuthorizer.new(
    client_id, SCOPE, token_store)
  user_id = 'default'
  credentials = authorizer.get_credentials(user_id)
  if credentials.nil?
    url = authorizer.get_authorization_url(
      base_url: OOB_URI)
    puts "Open the following URL in the browser and enter the " +
         "resulting code after authorization"
    puts url
    code = STDIN.gets
    credentials = authorizer.get_and_store_credentials_from_code(
      user_id: user_id, code: code, base_url: OOB_URI)
  end
  credentials
end


# Validate time string
def validate(str)
  puts !!Chronic.parse(str)
end

# Fetch the next n events for the user
def upcoming_events(service, n, offset=nil)
  offset = Chronic.parse(offset)
  if offset.nil?
    offset = Time.now
  end
  calendar_id = 'primary'
  response = service.list_events(calendar_id,
                                 max_results: n,
                                 single_events: true,
                                 order_by: 'startTime',
                                 time_min: offset.iso8601,
                                 time_max: (offset+86400).iso8601)

  if response.items.empty?
    puts "You have no upcoming events"
  else
    puts "You next #{response.items.length} upcoming events are:"
    response.items.each do |event|
      start = event.start.date || event.start.date_time
      puts "- #{event.summary} at #{start.strftime '%l:%M %P' }"
    end
  end

end

def add_new_event(service, options={})
  options[:attendees] = options[:attendees] || []
  if !options[:start_time]
    puts "ASKTIME"
    return
  end
  if !options[:end_time]
    puts "ASKENDTIME"
    return
  end
  if !options[:summary]
    puts "ASKSUMMARY"
    return
  end
  event = Google::Apis::CalendarV3::Event.new( {
    summary: options[:summary] || "Untitled Event",
    location: options[:location] || nil,
    description: options[:desc] || nil,
    start: {
      date_time: Chronic.parse(options[:start_time]).iso8601,
    },
    end: {
      date_time: Chronic.parse(options[:end_time]).iso8601,
    },
    attendees: options[:attendees].map {|e| {email: e}},
  })

  begin
    result = service.insert_event('primary', event)
    puts "Event created: #{result.html_link}"
  rescue
    puts "Something went wrong"
  end

end

# Initialize the API
service = Google::Apis::CalendarV3::CalendarService.new
service.client_options.application_name = APPLICATION_NAME
service.authorization = authorize

options = {}
args = OptionParser.new do |parser|
  parser.on("--next [N]", MAX_EVENTS) do |n|
    options[:next] = n
  end
  parser.on("--from [F]") do |f|
    options[:from] = f
  end
  parser.on("--start [S]") do |s|
    options[:start_time] = s
  end
  parser.on("--end [E]") do |e|
    options[:end_time] = e
  end
  parser.on("--summary [S]") do |s|
    options[:summary] = s
  end
  parser.on("--attendees [A]") do |a|
    options[:attendees] = a.split(',')
  end
  parser.on("--location [L]") do |l|
    options[:location] = l
  end
  parser.on("--desc [D]") do |d|
    options[:desc] = d
  end
end.parse!

if args.empty?
  upcoming_events(service, MAX_EVENTS)
elsif args[0] == "upcoming"
  upcoming_events(service, options[:next]||MAX_EVENTS, options[:from])
elsif args[0] == "new"
  add_new_event(service, options)
elsif args[0] == "validate-time"
  validate(args[1])
else
  upcoming_events(service, MAX_EVENTS)
end

