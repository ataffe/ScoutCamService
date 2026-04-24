# OwlCamService

A microservice built using django for managing rules for the owl cam system.

# API URL Reference

## Authentication

| Method | URL | Name |
|--------|-----|------|
| POST | `/v1/auth/register/` | `users:register` |
| POST | `/v1/auth/token/` | `users:token_obtain_pair` |
| POST | `/v1/auth/token/refresh/` | `users:token_refresh` |

## Users

| Method | URL | Name |
|--------|-----|------|
| GET | `/v1/users/` | `users:user_list` |
| GET | `/v1/user/<uuid:public_user_id>/` | `users:user_detail` |

## Cameras

| Method | URL | Name |
|--------|-----|------|
| GET, POST | `/v1/cameras/` | `camera:camera-list` |
| GET, PUT, PATCH, DELETE | `/v1/cameras/<public_camera_id>/` | `camera:camera-detail` |

## Rules

| Method | URL | Name |
|--------|-----|------|
| GET, POST | `/v1/cameras/<public_camera_id>/rules/` | `rules:camera-rules-list` |
| GET, PUT, PATCH, DELETE | `/v1/cameras/<public_camera_id>/rules/<public_rule_id>/` | `rules:camera-rules-detail` |

## Admin

| URL | Name |
|-----|------|
| `/admin/` | `admin:index` |
| `/admin/auth/group/` | `admin:auth_group_changelist` |
| `/admin/auth/group/add/` | `admin:auth_group_add` |
| `/admin/auth/group/<id>/change/` | `admin:auth_group_change` |
| `/admin/auth/group/<id>/delete/` | `admin:auth_group_delete` |
| `/admin/auth/group/<id>/history/` | `admin:auth_group_history` |
