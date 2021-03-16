import { Component, OnInit, Input } from '@angular/core';

import { ContentState } from '../../search/search.state';
import { SearchContent } from '../../search/search.action';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent implements OnInit {
  @Select(ContentState.getContent)
  content: any;

  userParams = {
    type: 'article',
    cx: '07f7a2e8b0b662f50',
    query: 'python',
    // page: '',
    // region: '',
  };

  warpContent = [
    {
      title: '15 Free Python Courses for Beginners to Learn Online',
      description:
        'A curated list of some of the free online courses to learn Python.',
      cse_url:
        'https://medium.com/swlh/5-free-python-courses-for-beginners-to-learn-online-e1ca90687caf',
      image: 'https://miro.medium.com/max/840/1*RJMxLdTHqVBSijKmOO5MAg.jpeg',
      date: '12/08/2020',
      meta_article_author: 'https://javinpaul.medium.com',
      meta_author: 'javinpaul',
      meta_section: '',
      meta_site_name: 'Medium',
      meta_type: 'article',
    },
    {
      title: 'Python: 7 Important Reasons Why You Should Use Python',
      description:
        'According to the latest TIOBE Programming Community Index, Python is one of the top 10 popular programming languages of 2017. Python is a\u2026',
      cse_url:
        'https://medium.com/@mindfiresolutions.usa/python-7-important-reasons-why-you-should-use-python-5801a98a0d0b',
      image: 'https://miro.medium.com/max/1140/1*WizgUsFeUgISS7vkFl4dEA.jpeg',
      date: '10/03/2017',
      meta_article_author: 'https://medium.com/@mindfiresolutions.usa',
      meta_author: 'Mindfire Solutions',
      meta_section: '',
      meta_site_name: 'Medium',
      meta_type: 'article',
    },
    {
      title: '12 Websites to Learn Python Programming for FREE',
      description:
        'Hello guys, if you are here then let me first congratulate you for making the right decision to learn Python programming language, the\u2026',
      cse_url:
        'https://medium.com/javarevisited/10-free-python-tutorials-and-courses-from-google-microsoft-and-coursera-for-beginners-96b9ad20b4e6',
      image: 'https://miro.medium.com/max/840/1*RJMxLdTHqVBSijKmOO5MAg.jpeg',
      date: '12/09/2020',
      meta_article_author: 'https://javinpaul.medium.com',
      meta_author: 'javinpaul',
      meta_section: '',
      meta_site_name: 'Medium',
      meta_type: 'article',
    },
    {
      title: 'Python at Netflix',
      description:
        'By Pythonistas at Netflix, coordinated by Amjith Ramanujam and edited by Ellen Livengood',
      cse_url:
        'https://medium.com/netflix-techblog/python-at-netflix-bba45dae649e',
      image: 'https://miro.medium.com/max/601/1*PPIp7twJJUknfohZqtL8pQ.png',
      date: '30/04/2019',
      meta_article_author: 'https://netflixtechblog.medium.com',
      meta_author: 'Netflix Technology Blog',
      meta_section: '',
      meta_site_name: 'Medium',
      meta_type: 'article',
    },
    {
      title: 'Python Lists and List Manipulation',
      description:
        'Before starting, I should mention that the code in this blog post and in the video above is available on my github.',
      cse_url:
        'https://medium.com/@GalarnykMichael/python-basics-6-lists-and-list-manipulation-a56be62b1f95',
      image: 'https://miro.medium.com/max/310/1*noxS-kGyde8dhaTXfKMTKg.png',
      date: '11/12/2019',
      meta_article_author: 'https://medium.com/@GalarnykMichael',
      meta_author: 'Michael Galarnyk',
      meta_section: '',
      meta_site_name: 'Medium',
      meta_type: 'article',
    },
    {
      title: 'code_swarm - Python',
      description:
        'Visualizing the commit history of the Python scripting language project.  Project page: http://vis.cs.ucdavis.edu/~ogawa/codeswarm/  Open source: http://code.google.com/p/codeswarm  Music: "Overflight"\u2026',
      cse_url: 'https://medium.com/media/176efd03c2b4aac3c843fc47c3fa8515/href',
      image:
        'https://i.vimeocdn.com/filter/overlay?src0=https%3A%2F%2Fi.vimeocdn.com%2Fvideo%2F21009317_1280x965.jpg&src1=https%3A%2F%2Ff.vimeocdn.com%2Fimages_v6%2Fshare%2Fplay_icon_overlay.png',
      date: '30/05/2008',
      meta_article_author: '',
      meta_author: '',
      meta_section: '',
      meta_site_name: 'Vimeo',
      meta_type: 'video.other',
    },
    {
      title: 'Python at Netflix',
      description:
        'Python\u2019s footprint in our environment continues to increase',
      cse_url:
        'https://medium.com/netflix-techblog/python-at-netflix-86b6028b3b3e',
      image: '',
      date: '20/09/2018',
      meta_article_author: 'https://netflixtechblog.medium.com',
      meta_author: 'Netflix Technology Blog',
      meta_section: '',
      meta_site_name: 'Medium',
      meta_type: 'article',
    },
    {
      title: 'PCA using Python (scikit-learn)',
      description:
        'My last tutorial went over Logistic Regression using Python. One of the things learned was that you can speed up the fitting of a machine learning algorithm by changing the optimization algorithm. A\u2026',
      cse_url:
        'https://medium.com/@GalarnykMichael/pca-using-python-scikit-learn-e653f8989e60',
      image: 'https://miro.medium.com/max/1050/1*Gob8ZbScyM7hHUHjvrMJYg.png',
      date: '02/03/2021',
      meta_article_author: 'https://medium.com/@GalarnykMichael',
      meta_author: 'Michael Galarnyk',
      meta_section: '',
      meta_site_name: 'Medium',
      meta_type: 'article',
    },
    {
      title: 'Hypermodern Python',
      description:
        'A guide to modern Python tooling with a focus on simplicity and minimalism. This chapter covers setting up a project using Poetry and\u2026',
      cse_url: 'https://medium.com/@cjolowicz/hypermodern-python-d44485d9d769',
      image: 'https://miro.medium.com/max/1200/1*F1PgdlB3Ez-xek3oU7fQzw.jpeg',
      date: '26/03/2020',
      meta_article_author: 'https://medium.com/@cjolowicz',
      meta_author: 'Claudio Jolowicz',
      meta_section: '',
      meta_site_name: 'Medium',
      meta_type: 'article',
    },
    {
      title: 'Building A Logistic Regression in Python, Step by Step',
      description:
        'Logistic Regression is a Machine Learning classification algorithm that is used to predict the probability of a categorical dependent\u2026',
      cse_url:
        'https://medium.com/towards-data-science/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8',
      image: 'https://miro.medium.com/max/1163/1*LrA_HrggXM_BDfippYTVxQ.png',
      date: '27/02/2019',
      meta_article_author: 'https://actsusanli.medium.com',
      meta_author: 'Susan Li',
      meta_section: '',
      meta_site_name: 'Medium',
      meta_type: 'article',
    },
  ];

  allColumns: any;

  selectedContents: any[] = [];

  warpSelectedColumns: any[] = [];

  selectedExampleRow: any = {};

  isDisplayDialog = false;

  innerWidth: any;
  innerHeight: any;

  constructor(private store: Store) {}

  async ngOnInit(): Promise<void> {
    // await this.store.dispatch(new SearchContent(this.userParams)).toPromise();
    this.setInnerWidthHeightParameters();

    this.allColumns = [
      ...this.warpContent.reduce(
        (set, object) => (
          Object.keys(object).forEach((key) => set.add(key)), set
        ),
        new Set()
      ),
    ];

    const warpColumns: any[] = [];
    this.allColumns.forEach((element: any) => {
      warpColumns.push({
        field: element,
        header: element[0].toUpperCase() + element.slice(1),
      });
    });

    this.allColumns = warpColumns;

    this.warpSelectedColumns = this.allColumns;
  }

  @Input() get selectedColumns(): any[] {
    return this.warpSelectedColumns;
  }

  set selectedColumns(value: any[]) {
    // restore original order
    this.warpSelectedColumns = this.allColumns.filter((column: any) =>
      value.includes(column)
    );
  }

  displayDialog(rowData: any): any {
    this.isDisplayDialog = true;
    this.selectedExampleRow = rowData;
  }

  setInnerWidthHeightParameters(): any {
    this.innerWidth = window.innerWidth;
    this.innerHeight = window.innerHeight * 0.7;
  }
}
