/*
	Forty by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var	$window = $(window),
		$body = $('body'),
		$wrapper = $('#wrapper'),
		$header = $('#header'),
		$banner = $('#banner');

	// Breakpoints.
		breakpoints({
			xlarge:    ['1281px',   '1680px'   ],
			large:     ['981px',    '1280px'   ],
			medium:    ['737px',    '980px'    ],
			small:     ['481px',    '736px'    ],
			xsmall:    ['361px',    '480px'    ],
			xxsmall:   [null,       '360px'    ]
		});

	/**
	 * Applies parallax scrolling to an element's background image.
	 * @return {jQuery} jQuery object.
	 */
	$.fn._parallax = (browser.name == 'ie' || browser.name == 'edge' || browser.mobile) ? function() { return $(this) } : function(intensity) {

		var	$window = $(window),
			$this = $(this);

		if (this.length == 0 || intensity === 0)
			return $this;

		if (this.length > 1) {

			for (var i=0; i < this.length; i++)
				$(this[i])._parallax(intensity);

			return $this;

		}

		if (!intensity)
			intensity = 0.25;

		$this.each(function() {

			var $t = $(this),
				on, off;

			on = function() {

				$t.css('background-position', 'center 100%, center 100%, center 0px');

				$window
					.on('scroll._parallax', function() {

						var pos = parseInt($window.scrollTop()) - parseInt($t.position().top);

						$t.css('background-position', 'center ' + (pos * (-1 * intensity)) + 'px');

					});

			};

			off = function() {

				$t
					.css('background-position', '');

				$window
					.off('scroll._parallax');

			};

			breakpoints.on('<=medium', off);
			breakpoints.on('>medium', on);

		});

		$window
			.off('load._parallax resize._parallax')
			.on('load._parallax resize._parallax', function() {
				$window.trigger('scroll');
			});

		return $(this);

	};

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Clear transitioning state on unload/hide.
		$window.on('unload pagehide', function() {
			window.setTimeout(function() {
				$('.is-transitioning').removeClass('is-transitioning');
			}, 250);
		});

	// Fix: Enable IE-only tweaks.
		if (browser.name == 'ie' || browser.name == 'edge')
			$body.addClass('is-ie');

	// Scrolly.
		$('.scrolly').scrolly({
			offset: function() {
				return $header.height() - 2;
			}
		});

	// Tiles.
		var $tiles = $('.tiles > article');

		$tiles.each(function() {

			var $this = $(this),
				$image = $this.find('.image'), $img = $image.find('img'),
				$link = $this.find('.link'),
				x;

			// Image.

				// Set image.
					$this.css('background-image', 'url(' + $img.attr('src') + ')');

				// Set position.
					if (x = $img.data('position'))
						$image.css('background-position', x);

				// Hide original.
					$image.hide();

			// Link.
				if ($link.length > 0) {

					$x = $link.clone()
						.text('')
						.addClass('primary')
						.appendTo($this);

					$link = $link.add($x);

					$link.on('click', function(event) {

						var href = $link.attr('href');

						// Prevent default.
							event.stopPropagation();
							event.preventDefault();

						// Target blank?
							if ($link.attr('target') == '_blank') {

								// Open in new tab.
									window.open(href);

							}

						// Otherwise ...
							else {

								// Start transitioning.
									$this.addClass('is-transitioning');
									$wrapper.addClass('is-transitioning');

								// Redirect.
									window.setTimeout(function() {
										location.href = href;
									}, 500);

							}

					});

				}

		});

	// Header.
		if ($banner.length > 0
		&&	$header.hasClass('alt')) {

			$window.on('resize', function() {
				$window.trigger('scroll');
			});

			$window.on('load', function() {

				$banner.scrollex({
					bottom:		$header.height() + 10,
					terminate:	function() { $header.removeClass('alt'); },
					enter:		function() { $header.addClass('alt'); },
					leave:		function() { $header.removeClass('alt'); $header.addClass('reveal'); }
				});

				window.setTimeout(function() {
					$window.triggerHandler('scroll');
				}, 100);

			});

		}

	// Banner.
		$banner.each(function() {

			var $this = $(this),
				$image = $this.find('.image'), $img = $image.find('img');

			// Parallax.
				$this._parallax(0.275);

			// Image.
				if ($image.length > 0) {

					// Set image.
						$this.css('background-image', 'url(' + $img.attr('src') + ')');

					// Hide original.
						$image.hide();

				}

		});

	// Menu.
		var $menu = $('#menu'),
			$menuInner;

		$menu.wrapInner('<div class="inner"></div>');
		$menuInner = $menu.children('.inner');
		$menu._locked = false;

		$menu._lock = function() {

			if ($menu._locked)
				return false;

			$menu._locked = true;

			window.setTimeout(function() {
				$menu._locked = false;
			}, 350);

			return true;

		};

		$menu._show = function() {

			if ($menu._lock())
				$body.addClass('is-menu-visible');

		};

		$menu._hide = function() {

			if ($menu._lock())
				$body.removeClass('is-menu-visible');

		};

		$menu._toggle = function() {

			if ($menu._lock())
				$body.toggleClass('is-menu-visible');

		};

		$menuInner
			.on('click', function(event) {
				event.stopPropagation();
			})
			.on('click', 'a', function(event) {

				var href = $(this).attr('href');

				event.preventDefault();
				event.stopPropagation();

				// Hide.
					$menu._hide();

				// Redirect.
					window.setTimeout(function() {
						window.location.href = href;
					}, 250);

			});

		$menu
			.appendTo($body)
			.on('click', function(event) {

				event.stopPropagation();
				event.preventDefault();

				$body.removeClass('is-menu-visible');

			})
			.append('<a class="close" href="#menu">Close</a>');

		$body
			.on('click', 'a[href="#menu"]', function(event) {

				event.stopPropagation();
				event.preventDefault();

				// Toggle.
					$menu._toggle();

			})
			.on('click', function(event) {

				// Hide.
					$menu._hide();

			})
			.on('keydown', function(event) {

				// Hide on escape.
					if (event.keyCode == 27)
						$menu._hide();

			});
			// datepicker 열기 버튼을 클릭했을 때의 이벤트 핸들러
			document.getElementById('open-datepicker').addEventListener('click', function() {
				var datepicker = document.getElementById('datepicker');
				datepicker.focus(); // datepicker 열기
			});
			
			// 드랍다운 메뉴 토글 함수
			function toggleDropdown(id) {
				var dropdown = document.getElementById(id);
				if (dropdown.style.display === "none") {
					dropdown.style.display = "block";
				} else {
					dropdown.style.display = "none";
				}
				}
			// jQuery UI Datepicker를 주간(date range) 모드로 설정하는 예시
			$(function() {
				// 시작 날짜와 종료 날짜를 선택하는 입력 상자의 ID를 가져옵니다.
				var startDateInputId = '#start-date';
				var endDateInputId = '#end-date';
			
				// jQuery UI Datepicker를 시작 날짜와 종료 날짜 입력 상자에 적용합니다.
				$(startDateInputId).datepicker({
				dateFormat: 'yyyy-mm-dd',  // 선택한 날짜의 형식 설정
				onSelect: function(selectedDate) {
					// 시작 날짜를 선택했을 때의 동작
					var endDate = $(endDateInputId).datepicker('getDate');
					$(endDateInputId).datepicker('option', 'minDate', selectedDate);
				}
				});
			
				$(endDateInputId).datepicker({
				dateFormat: 'yyyy-mm-dd',  // 선택한 날짜의 형식 설정
				onSelect: function(selectedDate) {
					// 종료 날짜를 선택했을 때의 동작
					var startDate = $(startDateInputId).datepicker('getDate');
					$(startDateInputId).datepicker('option', 'maxDate', selectedDate);
				}
				});
			});
			$(function() {
				// 기존의 버튼과 일일(date) datepicker의 ID를 가져옵니다.
				var dailyDatepickerButtonId = '#daily-datepicker-button';
				var dailyDatepickerId = '#daily-datepicker';
			  
				// 시작 날짜와 종료 날짜를 선택하는 입력 상자의 ID를 가져옵니다.
				var startDateInputId = '#start-date';
				var endDateInputId = '#end-date';
			  
				// 주간(date range) datepicker를 초기화합니다.
				$(startDateInputId).datepicker({
				  dateFormat: 'yy-mm-dd',
				  onSelect: function(selectedDate) {
					var endDate = $(endDateInputId).datepicker('getDate');
					$(endDateInputId).datepicker('option', 'minDate', selectedDate);
					updateDailyDatepicker(selectedDate, endDate);
				  }
				});
			  
				$(endDateInputId).datepicker({
				  dateFormat: 'yy-mm-dd',
				  onSelect: function(selectedDate) {
					var startDate = $(startDateInputId).datepicker('getDate');
					$(startDateInputId).datepicker('option', 'maxDate', selectedDate);
					updateDailyDatepicker(startDate, selectedDate);
				  }
				});
			  
				// Datepicker 요소 가져오기
				var datepicker = document.getElementById("datepicker");

				// 주간 Datepicker 설정
				var currentDate = new Date();  // 현재 날짜
				var firstDayOfWeek = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() - currentDate.getDay());  // 현재 주의 첫째 날짜
				var lastDayOfWeek = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() + (6 - currentDate.getDay()));  // 현재 주의 마지막 날짜

				// 주간 Datepicker에 대한 옵션 설정
				var options = {
				dateFormat: "yy-mm-dd",  // 날짜 형식
				minDate: firstDayOfWeek,  // 최소 선택 가능한 날짜
				maxDate: lastDayOfWeek,  // 최대 선택 가능한 날짜
				beforeShowDay: function(date) {  // 각 날짜에 대한 스타일 설정
					var cssClass = "";
					if (date >= firstDayOfWeek && date <= lastDayOfWeek) {
					cssClass = "highlight";
					}
					return [true, cssClass];
				},
				onSelect: function(dateText, inst) {  // 날짜 선택 시 이벤트 처리
					// 선택한 날짜 처리
					console.log("선택한 날짜:", dateText);
				}
				};
			  
				// Datepicker 초기화
				$(datepicker).datepicker(options);
			  	});
			  
  
})(jQuery);