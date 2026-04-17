from django.db import models
from django.db.models.functions import Now


from tracker.models import Item, Unit
# from aion_calendar.models import Schedule

# Create your models here.


class Vision(models.Model):
    """
    Where lies the leading stars.
    I want to be a reader. tags: intellectual growth
      - consistent reading habit (enumerable)
      - high reading speed (enumerable)
      - active contributer to a reader's club (can be checked off the box)
      - good at reading out to others  (can be measured through books read out to others)
    I want to be a linux expert. tags: technical
      - learn one new thing daily (enumerable) goal
        - sub goal: get a command for each day
                    code a command from scratch each week (cat in c (simplified), dd in c (simplified) or some how dd works series)
      - create a consistent sharing schedule (enumerable)
        - go to blogger (google's site) and create a linux blog
        - post about your weekly explorations
      - create and share scripts (enumerable)
        - find daily frustrations and create scripts for them
      - build projects around what you learn to help others
        - setup scripts
        - update scripts
      - develop a reading habit
        - even 1 book a year read once every 2 days is a good thing
      - get out of your comfort zone
        - use gentoo
        - do linux from scratch
        - use arch
    I want to own emacs (this will last for ever)
      - one new thing about emacs daily (an emacs command or so)
      - one new lisp trick daily
      - a sheet to keep track of all these commands that you author
    I want to be a quant developer
      - Math and statistics
        - develop a curriculum
        - create a consistent turn up system
        - share knowledge
        - write programs to cement knowlege
        - build projects around written programs and write about the projects
      - CPP proficiency
        - read bjarne's book
      - Algo and ds understanding
        - leet code
        - quant guide book
        - 
      - Networking proficiency
    I want to make my own mobile apps
      - Learn react native
        - 
    I want to understand android
    I want to be etc.
    -- statement
    -- sub statements (description of what that means or what one needs to achieve to be that)

    Want to be healthy
     - water habit
       buy a water bottle
       1 cup daily, 2 cups daily, 1 l daily
     - wake up early habit 
     - sleep early habit
     - mobile usage control habit
     - hygiene habits
     - knowlege about health
       - reading habit
         - cooking, vegeterianism, alt medicines, dangers of sugar etc
       - outputting habit (maybe)

    Want to become better and finances
    - discipline to ascertain where u stand currently
    - logging expenses habit
    - saving habit
    - budgetting habit
    - sticking to the budget habit / discipline
    - reading about finance habit
    
    
    Want to grow spiritually
    - prayer habit
    - turning up for Bible habit
    - topical study completion discipline
    - service habits
      - donation habit
      - greeting habit
      - sharing gospel habit
    """
    name = models.CharField(max_length=1024)



class Progression(models.Model):
    """
    goal: do 5 ... daily for X days
    target: 5
    target_type: min
    progressions_and_durations (pnum:target:duration:success_%age_for_progression): 1:2:X:80, 2:3:X:85, 3:4.5:X:95, 4:5:X:100
    id
    name
    goal
    """
    name = models.CharField(max_length=1024)
    target_type = '' # qty,
    
    
class LevelDependencies:
    """
    id
    dependent level
    dependent on
    dependence criterion
    """
    pass
    

class Level(models.Model):
    """
    (id
    progression id
    tracker habit id
    trial num )
    target type
    start date
    end date
    current avg
    status : (succeeded, active, failed)
    success criteria: (avg for x days, consecutive turn up for x days)
    """
    progression = models.ForeignKey(Progression, null=True, blank=True, on_delete=models.CASCADE)
    habit_tracked = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE)
    trial_num = models.IntegerField(unique=True, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    current_avg = models.FloatField(null=True, blank=True)
    status = models.CharField(choices=[('s','succeeded'),('f','failed'),('a','active'),('u','unstarted'), ('m','maintenance')], default="u")


    def succeeded(self):
        pass
    



class HigherGoal(models.Model):
    higher_goal = models.CharField(max_length=1024)
    def __str__(self):
        return self.higher_goal

class GoalTrial(models.Model):
    # trial1: (goal history) goal_id, trial_number, end_status (success or failure)
    # trial2: (goal history) same goal id, trial_number, 
    pass





class Goal(models.Model):
    goal = models.CharField(max_length=1024, null=True, blank=True)
    name = models.CharField(max_length=1024) # (sleep for 8 hours every day for 5 days)
    progression_number = models.IntegerField(default=1)
    trial_number = models.IntegerField(default=1)
    higher_goal = models.ForeignKey(HigherGoal, on_delete=models.CASCADE, null=True, blank=True)
    goal_item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    goal_item_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True) # warn
    related_goals = models.ManyToManyField('self', blank=True)
    target_sampling_frequency = models.CharField(choices=[("daily","Daily"),('weekly',"Weekly")], default="daily")
    target_count_per_sample = models.IntegerField(blank=True, null=True) # for quantitative goals
    target_type = models.CharField(choices=[('min','minimum'),('max','maximum'),('exact','exact')], default='min')
    target_time = models.TimeField(null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    target_sample_count = models.IntegerField(blank=True, null=True) # how long should the goal last (can be inferred from end date)
    start_date = models.DateField(db_default=Now()) # when does the goal start to be active
    end_date = models.DateTimeField(blank=True, null=True) # deadline

    
    
    def __str__(self):
        return f" {self.name} | {self.higher_goal}"
