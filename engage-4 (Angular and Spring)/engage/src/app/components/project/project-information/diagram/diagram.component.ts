import { Component, OnInit, EventEmitter } from '@angular/core';
import * as d3 from 'd3';
import {ProjectsService} from '../../../../services/project/projects.service';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {Project} from '../../../../models/project/project';
import {EngagedOrganisation} from '../../../../models/project/engaged-organisation';
import {EngagedOrganisationsService} from '../../../../services/project/engaged-organisations.service';

@Component({
  selector: 'app-diagram',
  templateUrl: './diagram.component.html',
  styleUrls: ['./diagram.component.css']
})
export class DiagramComponent implements OnInit {
  project: Project;
  engagedOrganisations: EngagedOrganisation[] = [];
  members = [];
  categories = ['Business', 'Academia', 'Environment', 'Media', 'Society', 'Government'];
  selectedOrganisationChanged = new EventEmitter();

  level = [{
    name: 'Influencer',
    color: '#FFFFFF'
  }, {
    name: 'Prospect',
    color: '#EBF1DE'
  }, {
    name: 'Partner',
    color: '#FFEEB9'
  }, {
    name: 'Core',
    color: '#FFDB69'
  }];


  // Rendering parameters
  // container = 600;
  // size = 500;
  container = 700;
  size = 600;
  padding = 5;
  strokeWidth = 2;
  strokeColour = '#000000';
  pointSize = 7;
  pointLabelOffset = 10;

  selectedMember: string = '';
  selectedMemberCategory: string = '';
  selectedMemberLevel: string = '';

  previousSelectedOrganisation = null;
  selectedOrganisation = null;
  currentTooltip = null;


  constructor(
      private projectsService: ProjectsService,
      private route: ActivatedRoute,
      private engagedOrganisationsService: EngagedOrganisationsService,
      private router: Router
  ) { }

  ngOnInit(): void {
    this.selectedOrganisationChanged.subscribe(() => {
      d3.select(this.selectedOrganisation).transition().duration("200").attr('r', this.pointSize * 1.5);
      d3.select(this.previousSelectedOrganisation).transition().duration("200").attr('r', this.pointSize);
    })

    this.route.params.subscribe(
        (params: Params) => {
          this.project = this.projectsService.findById(+params['id']);
          if (this.project !== null) {
            this.engagedOrganisations = this.engagedOrganisationsService.getAllForProject(this.project.id);
          }
        }
    );

    this.engagedOrganisationsService.engagedOrganisationsChanged.subscribe(() => {
      this.engagedOrganisations = this.engagedOrganisationsService.getAllForProject(this.project.id);
    })

    // adding the organisations to the diagram upon initialization of the component.
    this.addMembers();

    this.initDiagram();
  }

  initDiagram(): void {

    // Creating the SVG element
    const radar = d3.select('#radar')
        .append('svg')
        .attr('width', this.container)
        .attr('height', this.container);

    // Creating all the layers and quadrants
    this.createCirclesAndLines(radar);

    // // Creating the level labels (e.g. core, partner)
    // this.createLevelLabels(radar);

    // Calculating the position of points based on their category and level
    // It also includes a collision detection of points to avoid overlapping
    this.calculatePointsPosition();

    // Plotting points and labels in the diagram
    this.plotPoints(radar);

    // Plotting categories (e.g. Business, Academia)
    this.plotCategoryLabels(radar);

  }

  addMembers(): void {
    for (let i = 0; i < this.engagedOrganisations.length; i++) {
      if (this.engagedOrganisations[i].engagementLevel === 1) {
        this.members.push({name: this.engagedOrganisations[i].organisation.name, category: this.engagedOrganisations[i].category, level: 'Core'});
      } else if (this.engagedOrganisations[i].engagementLevel === 2) {
        this.members.push({name: this.engagedOrganisations[i].organisation.name, category: this.engagedOrganisations[i].category, level: 'Partner'});
      } else if (this.engagedOrganisations[i].engagementLevel === 3) {
        this.members.push({name: this.engagedOrganisations[i].organisation.name, category: this.engagedOrganisations[i].category, level: 'Prospect'});
      } else {
        this.members.push({name: this.engagedOrganisations[i].organisation.name, category: this.engagedOrganisations[i].category, level: 'Influencer'});
      }
    }
  }

  /**
   * Creating all the layers and quadrants
   */
  createCirclesAndLines(radar): void {
    radar.selectAll('circle')
        .data(this.level)
        .enter()
        .append('circle')
        .attr('stroke', '#A9A9A9')
        .attr('stroke-width', this.strokeWidth)
        .attr('stroke-dasharray', ("5, 5"))
        .attr('fill', (d) => {
          return d.color;
        })
        .attr('r', (d, i) => {
          return ((this.size / 2) / this.level.length) * (this.level.length - i);
        })
        .attr('cx', this.container / 2)
        .attr('cy', this.container / 2);

    radar.selectAll('line')
        .data(this.categories)
        .enter()
        .append('line')
        .attr('x1', (data, i) => {
          const deg = (360 / (this.categories.length)) * i;
          return (this.container / 2) + (this.size / 2) * Math.cos( deg * Math.PI / 180);
        })
        .attr('y1', (data, i) => {
          const deg = (360 / (this.categories.length)) * i;
          return (this.container / 2) + (this.size / 2) * Math.sin(deg * Math.PI / 180);
        })
        .attr('x2', this.container / 2)
        .attr('y2', this.container / 2)
        .attr('stroke', '#616161')
        .attr('stroke-width', this.strokeWidth);
  }

  /**
   * Creating the level labels (e.g. core, partner)
   */
  createLevelLabels(radar): void {
    const labelWidth = this.size * 0.12;
    const labelHeight = this.size * 0.04;
    const labelRadius = 5;

    radar.selectAll('rect')
        .data(this.level)
        .enter()
        .append('rect')
        .attr('x', () => {
          return this.container / 2 - labelWidth / 2;
        })
        .attr('y', (d, i) => {
          const interval = this.size / 2 / this.level.length;
          const offset = interval / 2 - labelHeight / 2;
          const containerOffset = (this.container - this.size) / 2;
          return interval * i + offset + containerOffset;
        })
        .attr('height', labelHeight)
        .attr('width', labelWidth)
        .attr('fill', 'white')
        .attr('rx', labelRadius);

    radar.selectAll('text')
        .data(this.level)
        .enter()
        .append('text')
        .text( (data) => {
          return data.name;
        })
        .attr('text-anchor', 'middle')
        .attr('y', (d, i) => {
          const interval = this.size / 2 / this.level.length;
          const offset = interval / 2 - labelHeight / 2;
          const containerOffset = (this.container - this.size) / 2;
          return interval * i + offset + labelHeight * 0.7 + containerOffset;
        })
        .attr('fill', (d, i) => {
          return d.color;
        })
        .attr('font-size', this.size * 0.023)
        .attr('x', (data, i) => {
          return this.container / 2;
        });
  }

  /**
   * Calculating the position of points based on their category and level
   * It also includes a collision detection of points to avoid overlapping
   */
  calculatePointsPosition(): void {
    this.members.forEach( (data) => {

      let x;
      let y;

      do {
        const radiansPerCategory = this.getRadiansPerCategory(null);
        const categoryPosition = this.getCategoryPositionByString(data.category);
        const categoryOffset = this.generateRandomNumber(this.getMemberPositionByString(data.name)) * radiansPerCategory;
        const angle = radiansPerCategory * (categoryPosition) + categoryOffset;

        // calculate the radius
        const pixelsPerCategory = (this.size / 2) / this.level.length;
        const levelPosition = this.getLevelPositionByString(data.level);
        const sectorOffset = this.generateRandomNumber(this.getMemberPositionByString(data.name)) * pixelsPerCategory;
        const radius = (this.size / 2) - (levelPosition * pixelsPerCategory) - sectorOffset;

        x = radius * Math.cos(angle) + this.container / 2;
        y = radius * Math.sin(angle) + this.container / 2;
      } while (this.hasCollision(x, y));

      data['x'] = x;
      data['y'] = y;

    });
  }

  /**
   * Plotting points and labels in the diagram
   */
  plotPoints(radar): void {
    const points = radar.append('g');
    let div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0)
        .style("position", "absolute")
        .style("text-align", "center")
        .style("width", "100px")
        .style("padding", "2px")
        .style("font", "13px sans-serif")
        .style("background", "lightsteelblue")
        .style("border", "0px")
        .style("border-radius", "8px")
        .style("pointer-events", "none")
        .style("padding", "5px")

    // points.selectAll('text')
    //     .data(this.members)
    //     .enter()
    //     .append('text')
    //     .text((d, i) => {
    //       return d.name;
    //     })
    //     .attr('memberCategory', (d, i) => {
    //     return d.category;
    //     })
    //     .attr('memberName', (d, i) => {
    //       return d.name;
    //     })
    //     .attr('memberLevel', (d, i) => {
    //      return d.level;
    //     })
    //     .attr('fill', 'black')
    //     .attr('font-size', this.size * 0.03)
    //     .attr('x', (d, i) => {
    //       return d.x + this.pointLabelOffset;
    //     })
    //     .attr('y', (d, i) => {
    //       return d.y + this.pointLabelOffset;
    //     });

    points.selectAll('circle')
        .data(this.members)
        .enter()
        .append('circle')
        .style("stroke-width", 1)
        .style("stroke", "black")
        .style("fill", "white")
        .attr('memberName', (d, i) => {
          return d.name;
        })
        .attr('memberCategory', (d, i) => {
          return d.category;
        })
       .attr('memberLevel', (d, i) => {
         return d.level;
        })
        .attr('r', this.pointSize)
        .attr('cx', (d, i) => {
          return d.x;
        })
        .attr('cy', (d, i) => {
          return d.y;
        })
        .on('click', (evt) => {
          if (evt.target.attributes.memberName) {
            if (this.selectedMember === '' && this.selectedMemberCategory === '' && this.selectedMemberLevel === '') {
              this.selectedMember = evt.target.attributes.memberName.value;
              this.selectedMemberCategory = evt.target.attributes.memberCategory.value;
              this.selectedMemberLevel = evt.target.attributes.memberLevel.value;

              if (this.selectedOrganisation !== null) {
                this.previousSelectedOrganisation = this.selectedOrganisation;
              }

              this.selectedOrganisation = evt.target;

              this.selectedOrganisationChanged.emit();

            } else if (this.selectedMember !== evt.target.attributes.memberName.value &&
                this.selectedMemberCategory !== evt.target.attributes.memberCategory.value
                && this.selectedMemberLevel  !== evt.target.attributes.memberLevel.value) {
              this.selectedMember = evt.target.attributes.memberName.value;
              this.selectedMemberCategory = evt.target.attributes.memberCategory.value;
              this.selectedMemberLevel = evt.target.attributes.memberLevel.value;

              if (this.selectedOrganisation !== null) {
                this.previousSelectedOrganisation = this.selectedOrganisation;
              }

              this.selectedOrganisation = evt.target;

              this.selectedOrganisationChanged.emit();

            }
            else {
              this.selectedMember = '';
              this.selectedMemberCategory = '';
              this.selectedMemberLevel = '';
              d3.select(this.selectedOrganisation).transition().duration("200").attr('r', this.pointSize);
              this.selectedOrganisation = null;
              this.previousSelectedOrganisation = null;
            }
          }
        })
        .on('mouseenter', (evt) => {
          if (evt.target.attributes.memberName) {
            document.body.style.cursor = 'pointer';
            d3.select(evt.target).transition().duration("200").attr('r', this.pointSize * 1.5);
            div.transition().duration(200).style("opacity", .9);
            div.html(evt.target.attributes.memberName.value)
                .style("left", (evt.pageX) + "px")
                .style("top", (evt.pageY - 55) + "px");
          }
        })
        .on('mouseleave', (evt) => {
          if (evt.target.attributes.memberName) {
            document.body.style.cursor = 'default';

            if (evt.target !== this.selectedOrganisation) {
              d3.select(evt.target).transition().duration("200").attr('r', this.pointSize);
            }

            div.transition().duration(300).style("opacity", 0);
          }
        });
  }


  /**
   * Plotting categories (e.g. Business, Academia)
   */
  plotCategoryLabels(radar): void {
    radar.selectAll('.category-label')
        .data(this.categories)
        .enter()
        .append('text')
        .attr('text-anchor', 'middle')
        .attr('class', 'category-label')
        .attr('fill', this.strokeColour)
        .text( (d) => {
          return d;
        })
        .attr('x', (d, i) => {
          // calculate the angle (radians)
          const radiansPerCategory = this.getRadiansPerCategory(null);
          const categoryPosition = this.getCategoryPositionByString(d);
          const categoryOffset = radiansPerCategory / 2;
          const angle = radiansPerCategory * categoryPosition + categoryOffset;
          // calculate the radius
          const radius = this.size / 2;
          const x = radius * Math.cos(angle);
          return x + this.container / 2;
        })
        .attr('y', (d, i) => {
          // calculate the angle (radians)
          const radiansPerCategory = this.getRadiansPerCategory(null);
          const categoryPosition = this.getCategoryPositionByString(d);
          const categoryOffset = radiansPerCategory / 2; // middle of the sector
          const angle = radiansPerCategory * categoryPosition + categoryOffset;
          // calculate the radius
          const radius = this.size / 2;
          const y = radius * Math.sin(angle);
          return y + this.container / 2 - 10;
        });
  }

  /**
   * Radians to Degrees
   */
  degrees(radians): number {
    return radians * 180 / Math.PI;
  }

  /**
   * Degrees to Radians
   */
  radians(degrees): number {
    return degrees * Math.PI / 180;
  }

  // tslint:disable-next-line:typedef
  getLevelPositionByString(level) {
    return this.level.findIndex((element) => {
      return element.name === level;
    });
  }

  // tslint:disable-next-line:typedef
  getCategoryPositionByString(category) {
    return this.categories.findIndex( (element) => {
      return element === category;
    });
  }

  // tslint:disable-next-line:typedef
  getMemberPositionByString(member) {
    return this.members.findIndex((element) => {
      return element.name === member;
    });
  }

  // tslint:disable-next-line:typedef
  getRadiansPerCategory(category) {
    return this.radians(360 / this.categories.length);
  }

  /**
   * used to randomly add members to in the chart
   */
  generateRandomNumber(i): number {
    let theNumber = Math.random();
    if (theNumber < 0.05) {
      theNumber = theNumber + 0.05;
    }
    if (theNumber > 0.95) {
      theNumber = theNumber - 0.05;
    }
    return theNumber;
  }

  /**
   * Iterate over members to check if a new point would generate collision
   */
  hasCollision(x, y): boolean {
    // tslint:disable-next-line:prefer-for-of
    for (let i = 0; i < this.members.length; i++) {
      if (this.checkDistanceBetweenMembers(x, this.members[i]['x'], y, this.members[i]['y']) < 10) {
        return true;
      }
    }
    return false;
  }

  /**
   * Get the distance between two points (members), used to check collision
   */
  checkDistanceBetweenMembers(x1: number, x2: number, y1: number, y2: number): number {
    const a = x2 - x1;
    const b = y2 - y1;
    return Math.sqrt(Math.pow(a, 2) + Math.pow(b, 2));
  }


  onCloseDetails() {
    this.selectedMember = '';
    this.selectedMemberCategory = '';
    this.selectedMemberLevel = '';

    d3.select(this.selectedOrganisation).transition().duration("200").attr('r', this.pointSize);

    this.selectedOrganisation = null;
    this.previousSelectedOrganisation = null;
  }
}
