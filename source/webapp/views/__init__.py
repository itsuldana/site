from .main_about_us import MainView
from .help import HelpView, send_email
from .lessons import LessonCreateView, LessonUpdateView, LessonDeleteView, LessonDetailView
from .module import ModuleCreateView, ModuleUpdateView
from .purchase import purchase_course, purchase_success, purchase_failure

from .module_test import (
    TestModulesList, TestDetailView,
    StartTestView, NextTestView,
    ResultView, TestModuleResultView, TestCaseDescriptionDetailView,
    DashboardView
    )

from .course import (
    CourseCreateView, CourseDetailView, CourseUpdateView, CourseListView, CoursesView, CoursePaidListView
)
