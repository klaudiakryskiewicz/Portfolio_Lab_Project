document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event  //jquery z wykorzystaniem ajaxa, zapytania bez przeładowania strony, django rest framework
     */

    // $('.help--slides-pagination').click(function(event) {
    //   event.preventDefault();
    //   var page_n = $(this).attr('href');
    //   // ajax
    //   $.ajax({
    //     type: "GET",
    //     url: "{% url 'index' %}", // name of url
    //     data: {
    //       page_n: page_n, //page_number
    //       csrfmiddlewaretoken: '{{ csrf_token }}',
    //     },
    //
    //
    //   });
    // });
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
      $.ajax({
        type: "GET",
        // url: "{% url 'index' %}", // name of url
        data: {
          page_n: page, //page_number
        },


      });
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // DONE: get data from inputs and show them in summary
      //  DATA - step 1 - categories
      let categories = document.querySelectorAll(".form-step-1");
      const categories_table = [];
      const categories_names = [];
      for (let el of categories) {
        if(el.checked === true){
             categories_table.push(parseInt(el['value']));
             categories_names.push(el.parentElement.children[2].textContent);
        }
      }
      console.log(categories_table);
      console.log(categories_names);

      //  DATA - step 2 - quantity
      let bags = document.querySelector(".form-step-2");
      let no_of_bags = parseInt(bags['value']);

      console.log(no_of_bags)


      //  DATA - step 3 - organisation
      let organisations = document.querySelectorAll(".form-step-3");
      let organisation = null;
      let organisation_name = null;
      for (let el of organisations) {
        if(el.checked === true){
             organisation = parseInt(el['value']);
             organisation_name = el.parentElement.children[2].children[1].innerHTML;
        }
      }

      if (this.currentStep == 3) {
        let inst_categories = document.querySelectorAll('#institution_categories');
        inst_categories.forEach(inst => {
          inst.parentElement.style.display = 'none';
          let inst_cat_ids = [];
          inst.value.toString().split(',').forEach(el => {
            let cat_id = parseInt(el, 10);
            inst_cat_ids.push(cat_id);

          });
          let includes = true;
          categories_table.forEach(id => {
            if (!inst_cat_ids.includes(id)) {
              includes = false;
            }
          });
          if (includes) {
            inst.parentElement.style.display = 'block';
          }
        });
      }


      //  DATA - step 4 - address
      const full_info ={}

      let address = document.querySelector(".form-step-4-address");
      full_info['address'] = address['value'];
      let city = document.querySelector(".form-step-4-city");
      full_info['city'] = city['value'];
      let postcode = document.querySelector(".form-step-4-postcode");
      full_info['postcode'] = postcode['value'];
      let phone = document.querySelector(".form-step-4-phone");
      full_info['phone'] = phone['value'];
      let date = document.querySelector(".form-step-4-date");
      full_info['date'] = date['value'];
      let time = document.querySelector(".form-step-4-time");
      full_info['time'] = time['value'];
      let more_info = document.querySelector(".form-step-4-more_info");
      full_info['more_info'] = more_info['value'];

      console.log(full_info);

      // summary
    document.querySelector('.summary-donation').innerText = no_of_bags + categories_names;
    document.querySelector('.summary-organisation').innerText = organisation_name;
    const addresshtml = document.querySelector('.summary-address').children;
    addresshtml[0].innerHTML = full_info['address'];
    addresshtml[1].innerHTML = full_info['city'];
    addresshtml[2].innerHTML = full_info['postcode'];
    addresshtml[3].innerHTML = full_info['phone'];
    const pickuphtml = document.querySelector('.summary-pickup').children;
    pickuphtml[0].innerHTML = full_info['date'];
    pickuphtml[1].innerHTML = full_info['time'];
    pickuphtml[2].innerHTML = full_info['more_info'];

    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();

      const token = document.getElementsByName("csrfmiddlewaretoken")[0];

      $.ajax({
            url : "/add-donation/",
            type: "POST",
            data: $("form").serialize(),
            dataType: 'json',
            success: function(){
              console.log('ok');
              window.location.assign("/form-confirmation/");
        }
      })
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
