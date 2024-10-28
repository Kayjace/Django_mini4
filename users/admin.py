from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    # 표시할 필드
    list_display = (
        "email_link",
        "nickname",
        "phone_number",
        "is_staff",
        "is_active",
        "is_admin",
    )

    # 검색할 수 있는 필드
    search_fields = ("email", "nickname", "phone_number")

    # 필터링 옵션
    list_filter = ("is_staff", "is_admin", "is_active")

    # 읽기 전용 필드 (리스트로 설정)
    readonly_fields = ("is_admin",)  # 튜플 또는 리스트로 설정해야 함

    # 이메일 클릭 시 링크로 이동하도록 설정
    def email_link(self, obj):
        return f'<a href="mailto:{obj.email}">{obj.email}</a>'

    email_link.allow_tags = True  # HTML 태그 허용
    email_link.short_description = "Email"  # 열 제목 설정


# User 모델을 어드민에 등록합니다.
admin.site.register(User, UserAdmin)
