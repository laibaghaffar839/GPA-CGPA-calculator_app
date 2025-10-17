import streamlit as st

def marks_to_gp(marks):
    m = float(marks)
    if m >= 85:
        return 4.00
    elif m >=80:
        return 3.66
    elif m >= 75:
        return 3.33
    elif m >= 70:
        return 3.00
    elif m >= 65:
        return 2.70
    elif m >= 60:
        return 2.30
    elif m >= 55:
        return 2.00
    elif m >= 50:
        return 1.70
    else:
        return 0.00
    
def calc_semester_gpa(courses):
    total_credits = 0.0
    total_weight_points = 0.0
    for credit, gp in courses:
        total_credits = + float(credit)
        total_weight_points = + float(credit) * float(gp)
    if total_credits == 0:
      return 0.0, 0.0, 0
    gpa = total_weight_points/total_credits
    return total_credits,total_weight_points, round(gpa,2)

st.title("GPA & CGPA Calculator")
st.write("Enter your marks or grade points and get semester GPA & overall CGPA.")

num_sem = st.number_input("Enter the number of Semesters:", min = 1, step = 1)

if "semesters" not in st.session_state:
    st.session_state.semesters = {}

if st.button("Start Calculation"):
    st.session_state.semesters = {}

for s in range(1, int(num_sem)+1):
    st.subheader(f"Semester {s}")
    num_courses = st.input_number(f"Number of Courses in Semester {s}:", min_value = 1, step = 1, key = f"courses {s}")

    courses = []
    for i in range(1, int(num_courses) + 1):
        st.markdown(f"**Course {i}**")
        credit = st.number_input(f"Credit hours for course {i} :", min_value=1, step=0.5, key=f"credit_{s}_{i}")
        mode = st.radio(f"Do you want to enter marks or grade point for course {i}?", ["Marks", "Grade Point"], key=f"mode_{s}_{i}")

        if mode == "Grade Point":
            gp = st.number_input(f"Enter grade point for course {i} (e.g., 3.66 or 4.0):", min_value=0.0, max_value=4.0, step=0.01, key=f"gp_{s}_{i}")
        else:
            marks = st.number_input(f"Enter marks (0-100) for course {i}:", min_value=0.0, max_value=100.0, step=0.1, key=f"marks_{s}_{i}")
            gp = marks_to_gp(marks)

        courses.append((credit, gp))

    if st.button(f"Calculate GPA for Semester {s}", key=f"calc_{s}"):
        sem_credits, sem_weighted, sem_gpa = calc_semester_gpa(courses)
        st.success(f"GPA for Semester {s}: {sem_gpa}")
        st.session_state.semesters[str(s)] = (sem_credits, sem_weighted, sem_gpa)

if st.button("Calculate Overall CGPA"):
    if len(st.session_state.semesters) == 0:
        st.warning("Please calculate at least one semester GPA first.")
    else:
        cumulative_credits = sum([v[0] for v in st.session_state.semesters.values()])
        cumulative_weighted_points = sum([v[1] for v in st.session_state.semesters.values()])
        if cumulative_credits == 0:
            st.error("Total credits are zero; cannot compute CGPA.")
        else:
            cgpa = cumulative_weighted_points / cumulative_credits
            st.subheader("Cumulative Summary")
            for i in sorted(st.session_state.semesters.keys(), key=lambda x: int(x)):
                sem = st.session_state.semesters[i]
                st.write(f"Semester {i}: GPA = {sem[2]}, Credits = {sem[0]}")
            st.success(f"Final CGPA = {round(cgpa, 2)}")



