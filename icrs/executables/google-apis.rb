#!/usr/bin/env ruby
require 'google/apis/calendar_v3'
require 'googleauth'
require 'googleauth/stores/file_token_store'

require 'fileutils'
require 'optparse'
require 'chronic'


MAX_EVENTS = 3

class Service

  $APPLICATION_NAME = 'Jatayu'
  $OOB_URI = 'urn:ietf:wg:oauth:2.0:oob'
  $SCOPE = Google::Apis::CalendarV3::AUTH_CALENDAR
  $CLIENT_SECRETS_PATH = File.join(Dir.pwd, 'executables', 'client_secret.json')
  $CREDENTIALS_PATH = File.join(Dir.home, '.credentials',
                               "calendar-ruby-quickstart.yaml")

  # Initialize the API and return a service variable
  def initialize(user_id)
    @user_id = user_id
  end

  def service
    s = Google::Apis::CalendarV3::CalendarService.new
    s.client_options.application_name = $APPLICATION_NAME
    s.authorization = authorize
    s
  end

  def fetch_authorizer
    FileUtils.mkdir_p(File.dirname($CREDENTIALS_PATH))

    client_id = Google::Auth::ClientId.from_file($CLIENT_SECRETS_PATH)
    token_store = Google::Auth::Stores::FileTokenStore.new(file: $CREDENTIALS_PATH)
    @authorizer = Google::Auth::UserAuthorizer.new(
      client_id, $SCOPE, token_store)
  end

  # Ensure valid credentials, either by restoring from the saved credentials
  # files or intitiating an OAuth2 authorization. If authorization is required,
  # the user's default browser will be launched to approve the request.
  #
  # @return [Google::Auth::UserRefreshCredentials] OAuth2 credentials
  def authorize
    fetch_authorizer
    @credentials = @authorizer.get_credentials(@user_id)
    if @credentials.nil?
      ask_for_authorization
    end
    @credentials
  end

  def authorize!(code)
    fetch_authorizer
    @credentials = @authorizer.get_and_store_credentials_from_code(
        user_id: @user_id, code: code, base_url: $OOB_URI)
    puts "I have received authorization to manage your calender."
  end

  def ask_for_authorization
    url = @authorizer.get_authorization_url(
      base_url: $OOB_URI)
    puts "Open the following URL in your browser and sene me the " +
         "resulting code after authorization"
    puts url
    exit
  end

end

# Validate time string
def validate(str)
  puts Chronic.parse(str)
end

# Fetch the next n events for the user
def upcoming_events(options)
  if !options[:user_id]
    puts "Please provide --user-id"
    return
  end

  s = Service.new(options[:user_id])
  service = s.service

  offset = Chronic.parse(options[:from]) || Time.now
  n = options[:next] || MAX_EVENTS

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

def add_new_event(options={})
  if !options[:user_id]
    puts "Please provide --user-id"
    return
  end

  s = Service.new(options[:user_id])
  service = s.service
  options[:attendees] = options[:attendees] || []
  #if !options[:start_time]
  #  puts "ASKTIME"
  #  return
  #end
  #if !options[:end_time]
  #  puts "ASKENDTIME"
  #  return
  #end
  #if !options[:summary]
  #  puts "ASKSUMMARY"
  #  return
  #end
  #
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

def authorize_token(options, token)
  if !options[:user_id]
    puts "Please provide --user-id"
    return
  end

  s = Service.new(options[:user_id])
  s.authorize!(token)
end

options = {}
args = OptionParser.new do |parser|
  parser.on("--user-id [U]") do |u|
    options[:user_id] = u
  end
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
  upcoming_events(options)
elsif args[0] == "authorize-token"
  authorize_token(options, args[1])
elsif args[0] == "upcoming"
  upcoming_events(options)
elsif args[0] == "new"
  add_new_event(options)
elsif args[0] == "validate-time"
  validate(args[1])
else
  upcoming_events(options)
end

