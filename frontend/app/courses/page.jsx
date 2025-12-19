"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { courseService } from "@/lib/api"
import { BookOpen, Users, Clock, Search, Filter } from "lucide-react"

export default function CoursesPage() {
  const [courses, setCourses] = useState([])
  const [searchQuery, setSearchQuery] = useState("")
  const [categoryFilter, setCategoryFilter] = useState("all")
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadCourses()
  }, [])

  const loadCourses = async () => {
    try {
      setIsLoading(true)
      const response = await courseService.getAllCourses()
      setCourses(response.data)
    } catch (error) {
      console.error("[v0] Error loading courses:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const filteredCourses = courses.filter((course) => {
    const matchesSearch =
      course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      course.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      course.instructor?.name.toLowerCase().includes(searchQuery.toLowerCase())

    const matchesCategory = categoryFilter === "all" || course.category === categoryFilter

    return matchesSearch && matchesCategory
  })

  const categories = ["all", ...new Set(courses.map((c) => c.category).filter(Boolean))]

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1">
        <section className="bg-gradient-to-br from-primary/10 to-accent/10 py-12">
          <div className="container mx-auto px-4">
            <h1 className="text-4xl font-bold mb-4 text-center">Jelajahi Kursus</h1>
            <p className="text-muted-foreground text-center mb-8 max-w-2xl mx-auto">
              Temukan kursus yang sesuai dengan minat dan kebutuhan belajar Anda
            </p>

            <div className="max-w-4xl mx-auto space-y-4">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                  <Input
                    placeholder="Cari kursus, instruktur..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                  <SelectTrigger className="w-full md:w-[200px]">
                    <Filter className="mr-2 h-4 w-4" />
                    <SelectValue placeholder="Kategori" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Semua Kategori</SelectItem>
                    {categories
                      .filter((c) => c !== "all")
                      .map((category) => (
                        <SelectItem key={category} value={category}>
                          {category}
                        </SelectItem>
                      ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
                <span>
                  Menampilkan {filteredCourses.length} dari {courses.length} kursus
                </span>
              </div>
            </div>
          </div>
        </section>

        <section className="py-12">
          <div className="container mx-auto px-4">
            {isLoading ? (
              <div className="text-center py-12">
                <p className="text-muted-foreground">Memuat kursus...</p>
              </div>
            ) : filteredCourses.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-muted-foreground">Tidak ada kursus ditemukan</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredCourses.map((course) => (
                  <Card key={course.id} className="hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="w-full h-40 bg-gradient-to-br from-primary/20 to-accent/20 rounded-md mb-4 flex items-center justify-center">
                        {course.thumbnail ? (
                          <img
                            src={course.thumbnail || "/placeholder.svg"}
                            alt={course.title}
                            className="w-full h-full object-cover rounded-md"
                          />
                        ) : (
                          <BookOpen className="w-16 h-16 text-primary" />
                        )}
                      </div>
                      <div className="flex items-center justify-between mb-2">
                        <CardTitle className="line-clamp-1 text-lg">{course.title}</CardTitle>
                        {course.category && (
                          <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded">
                            {course.category}
                          </span>
                        )}
                      </div>
                      <CardDescription className="line-clamp-2">{course.description}</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="space-y-2 text-sm text-muted-foreground">
                        <div className="flex items-center gap-2">
                          <Users className="w-4 h-4" />
                          <span>{course.total_students || 0} Mahasiswa</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Clock className="w-4 h-4" />
                          <span>Level: {course.level}</span>
                        </div>
                        {course.instructor && <p className="font-medium text-foreground">{course.instructor.name}</p>}
                      </div>

                      <Link href={`/courses/${course.id}`}>
                        <Button className="w-full">Lihat Detail</Button>
                      </Link>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </section>
      </main>

      <Footer />
    </div>
  )
}
