from .index import (
    MainView, filter_courses_main_page,
)

from .contact_us import (
    ContactUsView, send_email,
)

from .lessons import (
    LessonCreateView, LessonUpdateView,
    LessonDeleteView, LessonDetailView,
    ManageLessonsView,
)

from .module import (
    ModuleCreateView, ModuleUpdateView,
    ManageModulesView,
)

from .purchase import (
    PurchaseCreateView, PaymentQRView,
)


from .robots import (
    robots_txt,
)

from .module_test import (
    TestModulesList, TestDetailView,
    StartTestView, NextTestView,
    ResultView, TestModuleResultView,
    TestCaseDescriptionDetailView, DashboardView,
)

from .course import (
    CourseCreateView, CourseDetailView,
    CourseUpdateView, CourseListView,
    CoursesView, CoursePaidListView,
    filter_courses, RecommendedCoursesView,
)

from .certificate import (
    verify_certificate,
)
