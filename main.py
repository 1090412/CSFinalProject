import flet as ft
import pages.navigation as navigation
import pages.dashboard as dashboard
import pages.tableview as tableview



async def main(page:ft.Page):
    sidemenu_container = ft.Container()
    main_container = ft.Container()

    def on_route_change(event:ft.Event):
        path = page.route.strip("/").split("/")
        if path[0]=="":
            route="home"
        else:
            route=path[0]
        page.theme = navigation.themes[route]
        page.theme_mode = ft.ThemeMode.LIGHT
        page.appbar = navigation.create_appbar(page,route)
        sidemenu_container.content = navigation.create_sidemenu(page,route)
        if len(path)<2:
            main_container.content = dashboard.build_page(page,route)
        elif path[1]=="view":
            main_container.content = tableview.build_page(page,route)
        elif path[1]=="add":
            pass
        else:
            pass
        page.update()

    page.on_route_change = on_route_change
    page.add(
        ft.Row(
            expand=True,
            controls=[
                sidemenu_container,
                ft.VerticalDivider(width=5,thickness=2),
                ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=30,
                            content=main_container
                        )
                    ]
                )
            ]
        )
    )

    on_route_change(None)



if __name__=="__main__":
    ft.run(
        main,
        view=ft.AppView.WEB_BROWSER,
        port=8080
    )