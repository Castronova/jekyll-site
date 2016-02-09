# config valid only for Capistrano 3.1
# lock '3.2.1'

set :application, 'jekyll-site'
set :repo_url, "git@github.com:Castronova/jekyll-site.git"

# Default deploy_to directory is /var/www/my_app
set :deploy_to, "/home/castro/Documents/#{fetch(:application)}"

# Default value for :scm is :git
set :scm, :git

# Default value for :log_level is :debug
set :log_level, :debug

# Default value for keep_releases is 5
set :keep_releases, 5

# create file in student_updates
execute :mkdir, release_path.join('student_updates/updates')
execute :cp, '/home/testuser/weekly_updates/updates.md', release_path.join('student_updates/updates/testuser.md')


namespace :deploy do

  desc 'Restart application'
  task :restart do
    on roles(:app), in: :sequence, wait: 5 do

        
      # Your restart mechanism here, for example:
      # execute :touch, release_path.join('tmp/restart.txt')
  end
end
 
before :restart, :build_public do
   on roles(:app) do
       within release_path do
           execute '/home/castro/.rvm/gems/ruby-2.2.4/wrappers/jekyll',  "build"

#     within "#{deploy_to}/current" do
        #release_path do
        #execute 'jekyll',  "build --destination public"
 #       execute 'jekyll',  "build"
      end
   end
end
after :publishing, :restart

end
